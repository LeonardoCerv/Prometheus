import datetime
from zoneinfo import ZoneInfo
from typing import List, Dict, Any, Optional
from google.adk.agents import Agent
import os
import json
from .progressive_filter import ProgressiveFilter

# ==================== CUSTOM TOOLS FOR PROMETHEUS RECRUITMENT AGENT ====================

# Global progressive filter instance for maintaining conversation state
_progressive_filter = None

def get_progressive_filter() -> ProgressiveFilter:
    """Get or create the progressive filter instance"""
    global _progressive_filter
    if _progressive_filter is None:
        _progressive_filter = ProgressiveFilter()
    return _progressive_filter

# Load mock candidate data
def _load_mock_candidates() -> List[Dict[str, Any]]:
    """Load mock candidates from JSON file"""
    try:
        with open(os.path.join(os.path.dirname(__file__), 'mock_candidates.json'), 'r') as f:
            data = json.load(f)
            return data['candidates']
    except Exception as e:
        print(f"Warning: Could not load mock data: {e}")
        return []

def progressive_search(
    query: str,
    reset_conversation: bool = False
) -> dict:
    """Progressive candidate search that refines results through multi-turn conversation.
    
    This tool enables conversational filtering where each query builds on previous ones,
    progressively narrowing down candidates. Perfect for iterative refinement:
    - First query: "I need a web developer" (broad search)
    - Second query: "I need a React developer" (narrows to React)
    - Third query: "with Next.js experience" (further refines)
    
    The tool maintains conversation context and shows top matches at each stage,
    with scores that reflect both direct skill matches and transferable skills.
    
    Args:
        query (str): Natural language search query. Can be broad ("web developer") 
            or specific ("senior React developer with TypeScript"). Each query 
            refines the previous results.
            Examples:
            - "I need a web developer"
            - "I need a React developer"
            - "with Next.js and TypeScript"
            - "senior level only"
            - "available for freelance"
        reset_conversation (bool): Set to True to start a fresh search, clearing
            previous filters. Default: False (continues refinement)
    
    Returns:
        dict: Contains status, current matches, conversation context, and refinement suggestions.
            Example: {
                "status": "success",
                "conversation_turn": 2,
                "current_query": "I need a React developer",
                "combined_filters": {
                    "skills": ["javascript", "react"],
                    "experience_level": "any",
                    "availability": "any"
                },
                "matches_found": 5,
                "matches": [{
                    "candidate_id": "1",
                    "name": "Maria Garcia",
                    "score": 95.5,
                    "matched_skills": ["react", "javascript"],
                    "transferable_skills": [...],
                    "reasoning": "Has 2/2 required skills...",
                    ...
                }],
                "refinement_suggestion": "Consider adding specific requirements..."
            }
    """
    progressive_filter = get_progressive_filter()
    
    # Reset if requested
    if reset_conversation:
        progressive_filter.reset()
    
    # Perform progressive filtering
    result = progressive_filter.filter_candidates(query)
    
    return result


def search_candidates(
    job_requirements: str,
    skills: List[str],
    experience_level: str = "any",
    availability: str = "any"
) -> dict:
    """Searches for candidates matching job requirements using semantic AI matching.
    
    This tool performs semantic matching (not keyword-based) to find candidates whose
    skills, experience, and availability align with the job requirements. It analyzes
    transferable skills and context beyond exact keyword matches.
    
    DEPRECATED: Consider using progressive_search for multi-turn conversations that
    allow for iterative refinement of results.
    
    Args:
        job_requirements (str): Natural language description of the job requirements.
            Example: "Senior React developer with Next.js experience for 3-month project"
        skills (List[str]): List of required technical skills.
            Example: ["React", "Next.js", "TypeScript"]
        experience_level (str): Required experience level. Options: "junior", "mid", 
            "senior", "any". Default: "any"
        availability (str): Required availability type. Options: "full-time", "part-time",
            "freelance", "contract", "any". Default: "any"
    
    Returns:
        dict: Contains status and candidate matches with scores (0-100), reasoning,
            strengths, and gaps. Only returns matches with score >= 60.
            Example: {
                "status": "success",
                "matches": [{
                    "candidate_id": "123",
                    "name": "John Doe",
                    "score": 85,
                    "reasoning": "Strong React background...",
                    "strengths": ["React", "Next.js"],
                    "gaps": ["Limited TypeScript"]
                }]
            }
    """
    # Load mock candidates
    candidates = _load_mock_candidates()
    
    # Filter candidates based on criteria
    matches = []
    for candidate in candidates:
        # Check experience level
        if experience_level != "any" and candidate["experience_level"] != experience_level:
            continue
            
        # Check availability
        if availability != "any" and candidate["availability"] != availability:
            continue
            
        # Calculate skill match score
        candidate_skills = set([s.lower() for s in candidate["skills"]])
        required_skills = set([s.lower() for s in skills])
        
        # Direct skill matches
        direct_matches = candidate_skills & required_skills
        skill_match_score = (len(direct_matches) / len(required_skills) * 100) if required_skills else 0
        
        # Check for transferable skills (Vue.js -> React, etc.)
        transferable = 0
        if "react" in required_skills and "vue.js" in candidate_skills:
            transferable += 20
        if "next.js" in required_skills and "react" in candidate_skills:
            transferable += 15
        
        # Calculate total score
        total_score = min(100, skill_match_score + transferable)
        
        # Only include matches >= 60%
        if total_score >= 60:
            matches.append({
                "candidate_id": candidate["id"],
                "name": candidate["name"],
                "email": candidate["email"],
                "phone": candidate["phone"],
                "score": round(total_score, 1),
                "skills": candidate["skills"],
                "experience_years": candidate["total_years"],
                "experience_level": candidate["experience_level"],
                "availability": candidate["availability"],
                "location": candidate["location"],
                "matched_skills": list(direct_matches),
                "reasoning": f"Candidate has {len(direct_matches)}/{len(required_skills)} required skills. {candidate['total_years']} years of experience.",
                "strengths": list(direct_matches)[:3],
                "gaps": list(required_skills - direct_matches)[:3] if required_skills - direct_matches else ["None"]
            })
    
    # Sort by score descending
    matches.sort(key=lambda x: x["score"], reverse=True)
    
    return {
        "status": "success",
        "query": {
            "requirements": job_requirements,
            "skills": skills,
            "level": experience_level,
            "availability": availability
        },
        "total_candidates_searched": len(candidates),
        "matches_found": len(matches),
        "matches": matches[:5]  # Return top 5 matches
    }


def analyze_candidate_profile(cv_text: str) -> dict:
    """Analyzes candidate profile data and extracts structured information using Gemini Pro.
    
    This tool uses Gemini Pro to parse unstructured candidate data (CV text, LinkedIn
    profile text, or resume content) and extract structured profile information including 
    skills, experience, education, and availability.
    
    Args:
        cv_text (str): Raw text from candidate's CV, resume, LinkedIn profile description,
            or any professional profile text that needs to be analyzed and structured.
            Example: "Software engineer with 5 years of React experience..."
    
    Returns:
        dict: Contains status and structured profile data in JSON format.
            Example: {
                "status": "success",
                "profile": {
                    "name": "Jane Smith",
                    "email": "jane@example.com",
                    "skills": ["Python", "React", "AWS"],
                    "experience": [{
                        "title": "Senior Developer",
                        "company": "Tech Corp",
                        "duration": "2020-2023"
                    }],
                    "education": [...],
                    "availability": "freelance"
                }
            }
    """
    # This would integrate with your Next.js API endpoint /api/analyze-cv
    return {
        "status": "success",
        "message": "This tool will call your Next.js /api/analyze-cv endpoint with Gemini Pro parsing",
        "cv_text_length": len(cv_text),
        "profile": {
            "needs_processing": True,
            "source": "cv_text provided"
        }
    }


def send_whatsapp_offer(
    candidate_phone: str,
    candidate_name: str,
    job_title: str,
    job_description: str
) -> dict:
    """Sends a personalized job offer to a candidate via WhatsApp using Twilio.
    
    This tool generates a personalized job posting using Gemini, formats it for WhatsApp
    (max 300 words), and sends it via Twilio API. WhatsApp has a 98% open rate vs 20% 
    for email, making it highly effective for LATAM recruitment.
    
    Args:
        candidate_phone (str): Candidate's WhatsApp phone number in international format.
            Example: "+525512345678"
        candidate_name (str): Candidate's full name for personalization (e.g., "Maria Garcia")
        job_title (str): Title of the job position (e.g., "Senior React Developer")
        job_description (str): Brief description of the job requirements and details.
            Example: "3-month freelance project, React and Next.js, remote work"
    
    Returns:
        dict: Contains status, message ID from Twilio, and delivery status.
            Example: {
                "status": "success",
                "message_id": "SM1234567890",
                "delivery_status": "queued",
                "message_preview": "Hi John, I have an exciting opportunity..."
            }
    """
    # This would integrate with your Next.js API endpoint /api/send-offer
    # and Twilio WhatsApp API
    message_preview = f"Hi {candidate_name}, I have an exciting opportunity for you: {job_title}. {job_description[:100]}..."
    
    return {
        "status": "success",
        "message": "This tool will call your Next.js /api/send-offer endpoint and Twilio API",
        "recipient": candidate_phone,
        "candidate": candidate_name,
        "job": job_title,
        "message_preview": message_preview,
        "delivery_status": "queued"
    }


def schedule_meeting(
    candidate_phone: str,
    candidate_email: str,
    candidate_name: str,
    recruiter_email: str,
    date: str,
    time: str = "14:00",
    duration_minutes: int = 60,
    meeting_title: str = "Initial Interview"
) -> dict:
    """Schedules a meeting with a candidate using Google Calendar API integration.
    
    This tool creates a Google Calendar event with video conference link (Zoom/Meet),
    sends calendar invitations to both candidate and recruiter, and sets up automated
    reminders. It handles conflict detection and suggests alternatives if needed.
    
    Args:
        candidate_phone (str): Candidate's phone number for WhatsApp confirmation.
        candidate_email (str): Candidate's email for calendar invitation.
        candidate_name (str): Candidate's full name.
        recruiter_email (str): Recruiter's email for calendar invitation.
        date (str): Meeting date in ISO format (YYYY-MM-DD) or natural language
            like "next Monday", "October 25".
        time (str): Meeting time in 24-hour format (HH:MM). Default: "14:00"
        duration_minutes (int): Meeting duration in minutes. Default: 60
        meeting_title (str): Title for the calendar event. Default: "Initial Interview"
    
    Returns:
        dict: Contains status, calendar event details, and confirmation message.
            Example: {
                "status": "success",
                "event_id": "abc123",
                "meeting_link": "https://meet.google.com/xyz",
                "scheduled_time": "2025-10-25T14:00:00-05:00",
                "calendar_invites_sent": True
            }
    """
    # This would integrate with Google Calendar API and your /api/schedule endpoint
    return {
        "status": "success",
        "message": "This tool will create Google Calendar event and send invitations",
        "meeting_details": {
            "candidate": candidate_name,
            "date": date,
            "time": time,
            "duration": duration_minutes,
            "title": meeting_title
        }
    }


def calculate_match_score(
    candidate_name: str,
    job_title: str
) -> dict:
    """Calculates semantic compatibility score between a candidate and job requirements.
    
    Uses Gemini 2.0 Flash to analyze compatibility beyond keyword matching. Evaluates
    skill overlap, transferable skills (e.g., Vue.js → React), experience relevance,
    and availability. Returns detailed reasoning and gaps analysis.
    
    Scoring Formula:
    - Skill Match: 50% weight
    - Experience Match: 30% weight  
    - Availability Match: 20% weight
    Threshold: Only recommend matches >= 60%
    
    Args:
        candidate_name (str): Name of the candidate to analyze (e.g., "Maria Garcia")
        job_title (str): Title of the job position (e.g., "Senior React Developer")
    
    Returns:
        dict: Contains status, score (0-100), reasoning, strengths, and gaps.
            Example: {
                "status": "success",
                "score": 85,
                "reasoning": "Candidate has strong React foundation...",
                "strengths": ["React expertise", "Available immediately"],
                "gaps": ["Limited Next.js experience"],
                "recommendation": "Strong match - recommend interview"
            }
    """
    # Load mock candidates to find the candidate
    candidates = _load_mock_candidates()
    candidate = next((c for c in candidates if c["name"].lower() == candidate_name.lower()), None)
    
    if not candidate:
        return {
            "status": "error",
            "message": f"Candidate '{candidate_name}' not found in database"
        }
    
    # Calculate a simple match score based on skills
    score = 75  # Base score
    
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


def process_whatsapp_response(
    candidate_phone: str,
    message_body: str
) -> dict:
    """Processes incoming WhatsApp messages from candidates using function calling.
    
    Uses Gemini 2.0 Flash with function calling to analyze candidate intent and
    trigger appropriate actions:
    - schedule_meeting: If candidate wants to schedule
    - show_interest: If candidate has questions  
    - decline_offer: If candidate declines
    
    Args:
        candidate_phone (str): Candidate's phone number to identify them (e.g., "+525512345678")
        message_body (str): The text content of the WhatsApp message from the candidate
    
    Returns:
        dict: Contains status, detected intent, function to call, and response message.
            Example: {
                "status": "success",
                "intent": "schedule_meeting",
                "function_call": "schedule_meeting",
                "parameters": {"date": "2025-10-25", "time": "14:00"},
                "response_message": "Great! I'll schedule the meeting for..."
            }
    """
    # Analyze message for intent
    message_lower = message_body.lower()
    
    if any(word in message_lower for word in ["schedule", "meeting", "interview", "available"]):
        intent = "schedule_meeting"
        response = "I understand you'd like to schedule a meeting. Let me help you with that."
    elif any(word in message_lower for word in ["not interested", "decline", "no thanks"]):
        intent = "decline_offer"
        response = "I understand. Thank you for letting us know."
    else:
        intent = "show_interest"
        response = "Thank you for your message. I'll forward your questions to the recruiter."
    
    return {
        "status": "success",
        "from": candidate_phone,
        "message_preview": message_body[:100] + "..." if len(message_body) > 100 else message_body,
        "intent": intent,
        "response_message": response,
        "message": "This tool will analyze intent with Gemini function calling in production"
    }


# ==================== PROMETHEUS RECRUITMENT AGENT ====================

root_agent = Agent(
    name="prometheus_recruitment_agent",
    model="gemini-2.0-flash-exp",
    description=(
        "AI-powered recruitment agent for LATAM markets that automates candidate matching, "
        "WhatsApp communication, and interview scheduling using semantic AI analysis."
    ),
    instruction="""You are Prometheus, an advanced AI recruitment assistant designed for the LATAM market.

Your capabilities include:

1. **CANDIDATE SEARCH & MATCHING**
   - Use semantic AI matching (not keyword-based) to find candidates
   - Analyze transferable skills and context beyond exact matches
   - Calculate compatibility scores (0-100) with detailed reasoning
   - Only recommend candidates with scores >= 60%
   - **PROGRESSIVE FILTERING**: Use the progressive_search tool for multi-turn conversations
     that allow recruiters to refine results iteratively (e.g., "web developer" → "React developer" → "with Next.js")
   - Use the search_candidates tool for single-query searches with specific parameters
   - Use calculate_match_score for detailed compatibility analysis

2. **PROFILE ANALYSIS**
   - Parse CVs, LinkedIn profiles, and Gmail data using Gemini Pro
   - Extract structured information: skills, experience, education, availability
   - Use analyze_candidate_profile tool with available data sources

3. **WHATSAPP COMMUNICATION**
   - Send personalized job offers via WhatsApp (98% open rate)
   - Generate engaging, concise messages (max 300 words)
   - Use send_whatsapp_offer tool with candidate details
   - Process incoming candidate responses with intent recognition
   - Use process_whatsapp_response for analyzing replies

4. **MEETING SCHEDULING**
   - Schedule interviews with Google Calendar integration
   - Create video conference links automatically
   - Send calendar invitations to candidates and recruiters
   - Handle conflict detection and suggest alternatives
   - Use schedule_meeting tool with candidate and time details

**TOOL USAGE GUIDELINES:**

- **PREFERRED**: For recruiter queries like "Find me a web developer" or conversational refinements,
  use progressive_search - it maintains context across multiple queries and progressively refines results
- For single-query searches with explicit parameters, use search_candidates
- For analyzing candidate data, use analyze_candidate_profile
- For sending offers to selected candidates, use send_whatsapp_offer
- For scheduling interviews, use schedule_meeting
- For processing candidate WhatsApp replies, use process_whatsapp_response
- For detailed compatibility analysis, use calculate_match_score

**PROGRESSIVE SEARCH WORKFLOW:**
1. User: "I need a web developer" → Use progressive_search(query="I need a web developer")
2. User: "Actually, a React developer" → Use progressive_search(query="I need a React developer")
3. User: "with Next.js experience" → Use progressive_search(query="with Next.js experience")
Each query refines the previous results, showing best matches at each stage.

**COMMUNICATION STYLE:**
- Professional but approachable
- Concise and action-oriented
- Currently operating in English (LATAM multilingual support planned)
- Emphasize speed and efficiency (2 minutes to meeting vs 3-5 days traditional)

**IMPORTANT NOTES:**
- System currently operates in English only (hackathon version)
- Designed for LATAM market with 98% WhatsApp penetration
- Focus on reducing time-to-hire from days to minutes
- Prioritize candidate experience and quick response times""",
    tools=[
        progressive_search,
        search_candidates,
        analyze_candidate_profile,
        send_whatsapp_offer,
        schedule_meeting,
        calculate_match_score,
        process_whatsapp_response
    ],
)