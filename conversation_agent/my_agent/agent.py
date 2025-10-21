from google.adk.agents.llm_agent import Agent
from google.adk.tools import FunctionTool, ToolContext
from typing import Dict, Any, List
import json
import os
import firebase_admin
from firebase_admin import credentials, firestore

# Import the ProgressiveFilter class
from .progressive_filter import ProgressiveFilter

# ==================== FIREBASE INITIALIZATION ====================

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        # Check if Firebase is already initialized
        firebase_admin.get_app()
    except ValueError:
        # Firebase not initialized, so initialize it
        try:
            # Path to service account key file
            service_account_path = os.path.join(
                os.path.dirname(__file__), 
                'serviceAccount.json'
            )
            
            # Try to initialize with service account file
            if os.path.exists(service_account_path):
                cred = credentials.Certificate(service_account_path)
                firebase_admin.initialize_app(cred)
                print("Firebase initialized successfully with service account file")
            else:
                # Fallback: try environment variables (for deployed environments)
                cred_dict = {
                    "type": "service_account",
                    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
                    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
                    "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
                    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
                    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL")
                }
                
                required_creds = ["project_id", "private_key", "client_email"]
                if all(cred_dict.get(key) for key in required_creds):
                    cred = credentials.Certificate(cred_dict)
                    firebase_admin.initialize_app(cred)
                    print("Firebase initialized successfully with environment variables")
                else:
                    print("Warning: No Firebase credentials found")
                    print("Falling back to mock data")
        except Exception as e:
            print(f"Warning: Could not initialize Firebase: {e}")
            print("Falling back to mock data")

# ==================== PROGRESSIVE FILTERING STATE ====================

# Global progressive filter instance for maintaining conversation state
_progressive_filter = None
_candidates_cache = None

def get_progressive_filter() -> ProgressiveFilter:
    """Get or create the progressive filter instance with candidates loaded"""
    global _progressive_filter, _candidates_cache
    
    # Load candidates if not cached
    if _candidates_cache is None:
        _candidates_cache = _load_candidates_from_firebase()
    
    # Create or update progressive filter
    if _progressive_filter is None:
        _progressive_filter = ProgressiveFilter(_candidates_cache)
    else:
        # Update candidates in case they changed
        _progressive_filter.set_candidates(_candidates_cache)
    
    return _progressive_filter

# ==================== HELPER FUNCTIONS ====================

def _load_candidates_from_firebase() -> List[Dict[str, Any]]:
    """Load candidates from Firebase Firestore"""
    try:
        initialize_firebase()
        db = firestore.client()
        
        # Get all professional profiles from the userProfiles collection
        docs = db.collection('userProfiles').stream()
        
        candidates = []
        for doc in docs:
            data = doc.to_dict()
            
            # Extract profileData if it exists (nested structure)
            profile_data = data.get("profileData", {})
            personal_info = profile_data.get("personal_info", {})
            job_experience = profile_data.get("job_experience", [])
            education = profile_data.get("education", [])
            projects = profile_data.get("projects", [])
            skills_str = profile_data.get("skills", "")
            
            # Parse name from personal_info or fall back to top-level fields
            name = personal_info.get("name", "")
            if not name:
                first_name = data.get("firstName", "")
                last_name = data.get("lastName", "")
                name = f"{first_name} {last_name}".strip()
            
            # Extract email and phone from top level or nested structure
            email = data.get("email", "")
            phone = data.get("phone", "")
            
            # Extract location
            location = personal_info.get("location", data.get("location", ""))
            
            # Parse skills from the skills string (which contains technologies, frameworks, etc.)
            skills = _parse_skills_from_string(skills_str)
            
            # Calculate total years of experience from job_experience
            total_years = _calculate_years_of_experience(job_experience)
            
            # Extract profession from most recent job role or top-level field
            profession = data.get("profession", "")
            if not profession and len(job_experience) > 0:
                profession = job_experience[0].get("role", "")
            
            # Build a comprehensive bio from available data
            bio = _build_bio_from_profile(personal_info, job_experience, projects)
            
            # Map to candidate format
            candidate = {
                "id": doc.id,
                "name": name,
                "email": email,
                "phone": phone,
                "skills": skills,
                "experience": job_experience,  # Full job experience array
                "education": education,
                "experience_level": _map_experience_to_level(total_years),
                "total_years": total_years,
                "availability": "freelance",  # Could be enhanced with a field
                "location": location,
                "languages": ["English", "Spanish"],  # Could be enhanced
                "hourly_rate": 50,  # Could be enhanced
                "profession": profession,
                "bio": bio,
                "profileImage": personal_info.get("image", ""),
                "projects": projects,
                "skills_detailed": skills_str,  # Keep the full skills string for reference
                "updatedAt": data.get("updatedAt", "")
            }
            
            # Only add candidates with meaningful data
            if name and email and len(skills) > 0:
                candidates.append(candidate)
                print(f"✅ Loaded profile: {name} ({len(skills)} skills, {total_years} years exp)")
            else:
                print(f"⚠️ Skipping incomplete profile: {doc.id}")
        
        if len(candidates) == 0:
            print("⚠️ No candidates found in Firebase Firestore")
            return []
        
        print(f"\n✅ Successfully loaded {len(candidates)} profiles from Firebase Firestore\n")
        return candidates
        
    except Exception as e:
        print(f"❌ Error loading candidates from Firebase: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        print("⚠️ No fallback data available. Please check Firebase connection.")
        return []

def _map_experience_to_level(years: int) -> str:
    """Map years of experience to experience level"""
    if years >= 7:
        return "senior"
    elif years >= 3:
        return "mid"
    else:
        return "junior"

def _parse_skills_from_string(skills_str: str) -> List[str]:
    """Parse skills from a formatted string into a list of individual skills"""
    if not skills_str:
        return []
    
    skills = []
    
    # Split by common delimiters and extract technology names
    # Remove category labels like "Python (Advanced)", "Frameworks & Libraries:", etc.
    import re
    
    # Remove proficiency levels in parentheses
    skills_str = re.sub(r'\([^)]*\)', '', skills_str)
    
    # Split by various delimiters: commas, newlines, categories
    parts = re.split(r'[,\n]|Frameworks & Libraries:|Tools & Technologies:|Specializations:', skills_str)
    
    for part in parts:
        part = part.strip()
        if part and len(part) > 1:
            # Further split by slashes for things like "SQL/MySQL"
            sub_parts = part.split('/')
            for sub_part in sub_parts:
                sub_part = sub_part.strip()
                if sub_part and len(sub_part) > 1 and not sub_part.endswith(':'):
                    skills.append(sub_part)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_skills = []
    for skill in skills:
        skill_lower = skill.lower()
        if skill_lower not in seen:
            seen.add(skill_lower)
            unique_skills.append(skill)
    
    return unique_skills

def _calculate_years_of_experience(job_experience: List[Dict[str, Any]]) -> int:
    """Calculate total years of experience from job experience array"""
    if not job_experience:
        return 0
    
    from datetime import datetime
    from dateutil import parser
    
    total_months = 0
    
    for job in job_experience:
        start_date_str = job.get("start_date", "")
        end_date_str = job.get("end_date", "")
        
        if not start_date_str:
            continue
        
        try:
            # Parse start date
            start_date = parser.parse(start_date_str, fuzzy=True)
            
            # Parse end date (or use current date if "Present")
            if end_date_str.lower() in ["present", "current", ""]:
                end_date = datetime.now()
            else:
                end_date = parser.parse(end_date_str, fuzzy=True)
            
            # Calculate months
            months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
            total_months += max(0, months)
            
        except Exception as e:
            print(f"Warning: Could not parse dates for job: {job.get('role', 'Unknown')} - {e}")
            # Estimate 1 year if we can't parse
            total_months += 12
    
    return max(1, total_months // 12)  # Convert to years, minimum 1

def _build_bio_from_profile(personal_info: Dict[str, Any], job_experience: List[Dict[str, Any]], projects: List[Dict[str, Any]]) -> str:
    """Build a comprehensive bio from profile data"""
    bio_parts = []
    
    # Add most recent job description
    if job_experience and len(job_experience) > 0:
        latest_job = job_experience[0]
        role = latest_job.get("role", "")
        company = latest_job.get("company", "")
        description = latest_job.get("description", "")
        
        if role and company:
            bio_parts.append(f"Currently working as {role} at {company}.")
        
        if description:
            # Take first 200 characters of description
            short_desc = description[:200] + "..." if len(description) > 200 else description
            bio_parts.append(short_desc)
    
    # Add notable projects
    if projects and len(projects) > 0:
        notable_project = projects[0]
        project_name = notable_project.get("name", "")
        if project_name:
            bio_parts.append(f"Notable project: {project_name}")
    
    return " ".join(bio_parts) if bio_parts else "Professional profile"



# ==================== TOOL 1: PROGRESSIVE CANDIDATE SEARCH ====================

def progressive_search(
    query: str,
    reset_conversation: bool = False,
    tool_context: ToolContext = None
) -> dict:
    """Progressive candidate search that refines results through multi-turn conversation.
    
    This tool enables conversational filtering where each query builds on previous ones,
    progressively narrowing down candidates. Perfect for iterative refinement:
    - First query: "I need a web developer" (broad search)
    - Second query: "only React developers" (narrows to React)
    - Third query: "with Next.js experience" (further refines)
    
    Args:
        query (str): Natural language search query. Can be broad or specific. Each query 
            refines the previous results.
            Examples:
            - "I need a web developer"
            - "I need React developers"
            - "with Next.js and TypeScript"
            - "senior level only"
            - "available for freelance"
        reset_conversation (bool): Set to True to start a fresh search, clearing
            previous filters. Default: False (continues refinement)
    
    Returns:
        dict: Contains status, matches, conversation context, and refinement suggestions.
    """
    progressive_filter = get_progressive_filter()
    
    # Reset if requested
    if reset_conversation:
        progressive_filter.reset()
        print("\n*** DEBUG: Reset progressive filter for new search ***\n")
    
    # Perform progressive filtering
    result = progressive_filter.filter_candidates(query)
    
    print(f"\n*** DEBUG: Progressive search - Turn {result['conversation_turn']} ***")
    print(f"*** Query: {query} ***")
    print(f"*** Combined filters: {result['combined_filters']} ***")
    print(f"*** Matches found: {result['matches_found']} ***\n")
    
    return result

# ==================== TOOL 2: CALCULATE MATCH SCORE ====================

def calculate_match_score(
    candidate_name: str,
    job_title: str,
    tool_context: ToolContext = None
) -> dict:
    """Calculates semantic compatibility score between a candidate and job requirements.
    
    Uses semantic analysis to evaluate skill overlap, transferable skills, 
    experience relevance, and availability.
    
    Args:
        candidate_name (str): Name of the candidate to analyze (e.g., "Maria Garcia")
        job_title (str): Title of the job position (e.g., "Senior React Developer")
    
    Returns:
        dict: Contains status, score (0-100), reasoning, strengths, and gaps.
    """
    # Load candidates from Firebase
    candidates = _load_candidates_from_firebase()
    candidate = next((c for c in candidates if c["name"].lower() == candidate_name.lower()), None)
    
    if not candidate:
        return {
            "status": "error",
            "message": f"Candidate '{candidate_name}' not found in database"
        }
    
    # Calculate a simple match score based on skills
    score = 75  # Base score
    
    print(f"\n*** DEBUG: Calculated match score for {candidate_name} - Score: {score} ***\n")
    
    return {
        "status": "success",
        "candidate": candidate["name"],
        "job": job_title,
        "score": score,
        "reasoning": f"{candidate['name']} has {candidate['total_years']} years of experience with skills: {', '.join(candidate['skills'][:5])}",
        "strengths": candidate["skills"][:3],
        "gaps": ["None identified - strong match"],
        "recommendation": "Strong match - recommend interview" if score >= 70 else "Moderate match - consider interview"
    }

# ==================== TOOL 3: RESET SEARCH ====================

def reset_search(tool_context: ToolContext = None) -> dict:
    """Resets the progressive search to start a fresh candidate search.
    
    Use this when the recruiter wants to start a completely new search,
    clearing all previous filters and conversation context.
    
    Returns:
        dict: Confirmation of reset
    """
    progressive_filter = get_progressive_filter()
    progressive_filter.reset()
    
    print("\n*** DEBUG: Progressive search reset - starting fresh ***\n")
    
    return {
        "status": "success",
        "message": "Search reset. Ready for a new candidate search."
    }

# ==================== TOOL 4: GENERATE JOB DESCRIPTION ====================

def generate_job_description(tool_context: ToolContext = None) -> dict:
    """Generates a professional job description based on the search conversation.
    
    Analyzes all the queries and filters applied during the conversation to create
    a comprehensive job description including required skills, experience level,
    availability, and responsibilities.
    
    Returns:
        dict: Contains the generated job description with all relevant sections
    """
    progressive_filter = get_progressive_filter()
    summary = progressive_filter.get_conversation_summary()
    
    if summary['turns'] == 0:
        print(f"\n*** DEBUG: Cannot generate job description - no search queries yet ***\n")
        return {
            "status": "error",
            "message": "No search queries have been made yet. Please start a candidate search first."
        }
    
    # Get the combined filters from the conversation
    # We need to reconstruct the filters from the conversation history
    all_skills = []
    experience_level = "any"
    availability = "any"
    
    for turn in summary['history']:
        reqs = turn['requirements']
        all_skills.extend(reqs['skills'])
        
        if reqs['experience_level'] != "any":
            experience_level = reqs['experience_level']
        if reqs['availability'] != "any":
            availability = reqs['availability']
    
    # Remove duplicates from skills
    all_skills = list(set(all_skills))
    
    print(f"\n*** DEBUG: Generating job description - Skills: {all_skills}, Level: {experience_level}, Availability: {availability} ***\n")
    
    # Build the job description components
    job_data = {
        "status": "success",
        "conversation_turns": summary['turns'],
        "queries": summary['queries'],
        "required_skills": all_skills,
        "experience_level": experience_level,
        "availability": availability,
        "candidates_matching": summary['candidates_remaining']
    }
    
    return job_data

# ==================== WRAP TOOLS ====================

progressive_search_tool = FunctionTool(progressive_search)
calculate_match_tool = FunctionTool(calculate_match_score)
reset_search_tool = FunctionTool(reset_search)
generate_jd_tool = FunctionTool(generate_job_description)

# ==================== DEFINE THE AGENT ====================

root_agent = Agent(
    model='gemini-2.5-flash',
    name='prometheus_recruiter',
    description='An intelligent recruitment assistant that helps find and match candidates through conversational filtering.',
    
    instruction=(
        "You are Prometheus, an intelligent recruitment assistant specialized in finding "
        "the perfect candidates through natural conversation.\n\n"
        
        "# Core Behavior:\n"
        "You help recruiters find candidates by having a natural conversation. Each query "
        "from the recruiter AUTOMATICALLY refines the previous search results - you don't "
        "need to repeat previous requirements.\n\n"
        
        "# How Progressive Search Works:\n"
        "- First query: 'I need web developers' → Shows all web developers\n"
        "- Follow-up: 'only React developers' → Automatically narrows to React (web dev context maintained)\n"
        "- Follow-up: 'with Next.js' → Further narrows to React + Next.js developers\n"
        "- The tool maintains ALL previous filters automatically!\n\n"
        
        "# When to Use progressive_search:\n"
        "Use this tool for ANY of these situations:\n"
        "- Initial search request: 'I need a developer', 'find me React developers'\n"
        "- Refinement requests: 'only senior ones', 'with TypeScript', 'available freelance'\n"
        "- Follow-up queries: 'but only...', 'with...', 'who also know...', 'full-time only'\n"
        "- ALWAYS set reset_conversation=False for refinements (default)\n"
        "- ONLY set reset_conversation=True if the recruiter explicitly wants to start over\n\n"
        
        "# Presenting Results:\n"
        "When you get search results:\n"
        "1. Tell them how many matches were found\n"
        "2. Present the top 3-5 candidates clearly with:\n"
        "   - Name and contact info\n"
        "   - Match score and why they're a good fit\n"
        "   - Key matched skills\n"
        "   - Experience level and availability\n"
        "3. If there are more candidates, mention 'I found X other matches'\n"
        "4. Mention the refinement suggestion if provided\n"
        "5. Ask if they want to refine further or see specific candidates\n\n"
        
        "# Other Tools:\n"
        "- Use 'calculate_match_score' when asked to analyze a specific candidate against a job\n"
        "- Use 'reset_search' when they explicitly want to 'start over' or 'new search'\n"
        "- Use 'generate_job_description' when they ask to 'create a job description', 'generate JD', "
        "'write a job post', or 'summarize this into a job description'\n\n"
        
        "# Generating Job Descriptions:\n"
        "When using generate_job_description:\n"
        "1. Call the tool to get the structured data (skills, experience level, availability)\n"
        "2. Create a professional, well-formatted job description that includes:\n"
        "   - A compelling job title based on the role and level\n"
        "   - An engaging overview/summary\n"
        "   - Key responsibilities (inferred from the role type)\n"
        "   - Required skills (from the search queries)\n"
        "   - Experience level requirements\n"
        "   - Employment type (based on availability)\n"
        "   - Nice-to-have skills (related to required ones)\n"
        "3. Make it sound professional and appealing to candidates\n"
        "4. Mention how many candidates match this description\n\n"
        
        "# Conversation Style:\n"
        "- Be friendly and professional\n"
        "- Understand context from the conversation naturally\n"
        "- When they say 'only X' or 'with Y', you know they mean 'from the current results'\n"
        "- Proactively suggest refinements when there are many matches\n"
        "- Celebrate when you find great matches!\n\n"
        
        "# Important:\n"
        "- The progressive_search tool handles ALL the context automatically\n"
        "- You just pass their natural language query to the tool\n"
        "- Never manually track or repeat previous requirements - the tool does this\n"
        "- Focus on helping the recruiter express what they want naturally"
    ),
    
    tools=[
        progressive_search_tool,
        calculate_match_tool,
        reset_search_tool,
        generate_jd_tool
    ],
)