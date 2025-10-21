"""
Example client for Prometheus Recruitment API
Shows how to integrate the API in your application
"""

import requests
from typing import List, Dict, Any, Optional

class PrometheusClient:
    """Client for interacting with the Prometheus Recruitment API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def search_candidates(self, query: str, reset: bool = False) -> Dict[str, Any]:
        """
        Search for candidates with a natural language query.
        
        Args:
            query: Natural language search query
            reset: Whether to reset the conversation and start fresh
            
        Returns:
            Search results with matches and refinement suggestions
        """
        response = self.session.post(
            f"{self.base_url}/api/search",
            json={"query": query, "reset_conversation": reset}
        )
        response.raise_for_status()
        return response.json()
    
    def calculate_match(self, candidate_name: str, job_title: str) -> Dict[str, Any]:
        """
        Calculate match score between a candidate and job position.
        
        Args:
            candidate_name: Name of the candidate
            job_title: Job title or position
            
        Returns:
            Match score, reasoning, strengths, and gaps
        """
        response = self.session.post(
            f"{self.base_url}/api/match-score",
            json={"candidate_name": candidate_name, "job_title": job_title}
        )
        response.raise_for_status()
        return response.json()
    
    def reset_search(self) -> Dict[str, Any]:
        """Reset the search conversation."""
        response = self.session.post(f"{self.base_url}/api/reset")
        response.raise_for_status()
        return response.json()
    
    def generate_job_description(self) -> Dict[str, Any]:
        """Generate a job description from search conversation."""
        response = self.session.post(f"{self.base_url}/api/job-description")
        response.raise_for_status()
        return response.json()
    
    def get_conversation_state(self) -> Dict[str, Any]:
        """Get current conversation state and history."""
        response = self.session.get(f"{self.base_url}/api/conversation-state")
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health status."""
        response = self.session.get(f"{self.base_url}/api/health")
        response.raise_for_status()
        return response.json()


def example_workflow():
    """Example workflow showing typical usage patterns"""
    
    # Initialize client
    client = PrometheusClient()
    
    print("="*70)
    print("  PROMETHEUS RECRUITMENT API - Example Workflow")
    print("="*70)
    
    # Check API health
    print("\n1️⃣  Checking API health...")
    health = client.health_check()
    print(f"✅ API Status: {health['status']}")
    
    # Start a new search
    print("\n2️⃣  Starting initial search for React developers...")
    result = client.search_candidates("I need a React developer", reset=True)
    print(f"✅ Found {result['matches_found']} matches")
    print(f"   Suggestion: {result['refinement_suggestion']}")
    
    # Show top 3 candidates
    if result['matches']:
        print("\n   Top 3 Candidates:")
        for i, candidate in enumerate(result['matches'][:3], 1):
            print(f"\n   {i}. {candidate['name']} - Score: {candidate['score']}")
            print(f"      Email: {candidate['email']}")
            print(f"      Skills: {', '.join(candidate['skills'][:5])}")
            print(f"      Experience: {candidate['experience_years']} years ({candidate['experience_level']})")
            print(f"      Availability: {candidate['availability']}")
    
    # Refine search - add experience level
    print("\n3️⃣  Refining search to senior level only...")
    result = client.search_candidates("only senior level")
    print(f"✅ Narrowed to {result['matches_found']} senior matches")
    
    # Further refinement - add specific skill
    print("\n4️⃣  Further refinement - must have Next.js...")
    result = client.search_candidates("with Next.js experience")
    print(f"✅ Found {result['matches_found']} senior React + Next.js developers")
    
    # Get conversation state
    print("\n5️⃣  Checking conversation state...")
    state = client.get_conversation_state()
    print(f"✅ Conversation turns: {state['turns']}")
    print(f"   Queries: {state['queries']}")
    print(f"   Candidates remaining: {state['candidates_remaining']}")
    
    # Calculate match score for a specific candidate
    if result['matches']:
        candidate_name = result['matches'][0]['name']
        print(f"\n6️⃣  Calculating match score for {candidate_name}...")
        match = client.calculate_match(candidate_name, "Senior React/Next.js Developer")
        print(f"✅ Match Score: {match['score']}")
        print(f"   Reasoning: {match['reasoning']}")
        print(f"   Recommendation: {match['recommendation']}")
    
    # Generate job description
    print("\n7️⃣  Generating job description from search...")
    job_desc = client.generate_job_description()
    if job_desc['status'] == 'success':
        print("✅ Job Description Generated:")
        print(f"   Required Skills: {', '.join(job_desc['required_skills'])}")
        print(f"   Experience Level: {job_desc['experience_level']}")
        print(f"   Availability: {job_desc['availability']}")
        print(f"   Matching Candidates: {job_desc['candidates_matching']}")
    
    # Reset for new search
    print("\n8️⃣  Resetting search for a new query...")
    reset_result = client.reset_search()
    print(f"✅ {reset_result['message']}")
    
    # Start completely new search
    print("\n9️⃣  Starting new search for Python developers...")
    result = client.search_candidates("I need Python developers for backend work")
    print(f"✅ Found {result['matches_found']} Python developers")
    
    print("\n" + "="*70)
    print("  ✅ Workflow completed successfully!")
    print("="*70)
    print()


def example_freelance_search():
    """Example: Finding freelance React developers"""
    client = PrometheusClient()
    
    print("\n" + "="*70)
    print("  Example: Finding Freelance React Developers")
    print("="*70)
    
    # Search flow
    result = client.search_candidates("React developers", reset=True)
    print(f"\n1. Initial search: {result['matches_found']} React developers")
    
    result = client.search_candidates("available for freelance")
    print(f"2. Freelance only: {result['matches_found']} matches")
    
    result = client.search_candidates("with TypeScript")
    print(f"3. + TypeScript: {result['matches_found']} matches")
    
    # Show results
    print("\n📋 Final Results:")
    for candidate in result['matches'][:5]:
        rate = candidate.get('hourly_rate', 'N/A')
        print(f"\n• {candidate['name']} - Score: {candidate['score']}")
        print(f"  Hourly Rate: ${rate}/hr" if rate != 'N/A' else "  Hourly Rate: Not specified")
        print(f"  Skills: {', '.join(candidate['matched_skills'])}")


def example_fulltime_search():
    """Example: Finding full-time Python developers"""
    client = PrometheusClient()
    
    print("\n" + "="*70)
    print("  Example: Finding Full-Time Python Developers")
    print("="*70)
    
    result = client.search_candidates("Python backend developers", reset=True)
    print(f"\n1. Initial search: {result['matches_found']} Python developers")
    
    result = client.search_candidates("full-time availability")
    print(f"2. Full-time only: {result['matches_found']} matches")
    
    result = client.search_candidates("with Django or FastAPI")
    print(f"3. + Django/FastAPI: {result['matches_found']} matches")
    
    # Show results
    print("\n📋 Final Results:")
    for candidate in result['matches'][:5]:
        salary = candidate.get('salary_expectation', 'N/A')
        print(f"\n• {candidate['name']} - Score: {candidate['score']}")
        print(f"  Salary Expectation: ${salary:,}" if salary != 'N/A' else "  Salary Expectation: Not specified")
        print(f"  Experience: {candidate['experience_years']} years ({candidate['experience_level']})")


if __name__ == "__main__":
    try:
        # Run main workflow
        example_workflow()
        
        # Run specific examples
        example_freelance_search()
        example_fulltime_search()
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to API server")
        print("   Make sure the server is running at http://localhost:8000")
        print("   Start the server with: python main.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
