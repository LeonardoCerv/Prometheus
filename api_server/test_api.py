"""
Test script for Prometheus Recruitment API
Demonstrates all endpoints with example requests
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_response(response: requests.Response):
    """Pretty print API response"""
    print(f"\nStatus Code: {response.status_code}")
    print("\nResponse:")
    print(json.dumps(response.json(), indent=2))

def test_health_check():
    """Test health check endpoint"""
    print_section("1. Health Check")
    response = requests.get(f"{BASE_URL}/api/health")
    print_response(response)

def test_root():
    """Test root endpoint"""
    print_section("2. Root / API Info")
    response = requests.get(f"{BASE_URL}/")
    print_response(response)

def test_progressive_search():
    """Test progressive search with multiple refinements"""
    print_section("3. Progressive Search - Initial Query")
    
    # First search
    response = requests.post(
        f"{BASE_URL}/api/search",
        json={
            "query": "I need a React developer",
            "reset_conversation": False
        }
    )
    print_response(response)
    
    # Refinement 1
    print_section("4. Progressive Search - Refinement (Senior Level)")
    response = requests.post(
        f"{BASE_URL}/api/search",
        json={
            "query": "only senior level",
            "reset_conversation": False
        }
    )
    print_response(response)
    
    # Refinement 2
    print_section("5. Progressive Search - Further Refinement (Next.js)")
    response = requests.post(
        f"{BASE_URL}/api/search",
        json={
            "query": "with Next.js experience",
            "reset_conversation": False
        }
    )
    print_response(response)

def test_conversation_state():
    """Test conversation state endpoint"""
    print_section("6. Get Conversation State")
    response = requests.get(f"{BASE_URL}/api/conversation-state")
    print_response(response)

def test_match_score():
    """Test match score calculation"""
    print_section("7. Calculate Match Score")
    response = requests.post(
        f"{BASE_URL}/api/match-score",
        json={
            "candidate_name": "Maria Garcia",
            "job_title": "Senior React Developer"
        }
    )
    print_response(response)

def test_job_description():
    """Test job description generation"""
    print_section("8. Generate Job Description")
    response = requests.post(f"{BASE_URL}/api/job-description")
    print_response(response)

def test_reset():
    """Test reset endpoint"""
    print_section("9. Reset Search")
    response = requests.post(f"{BASE_URL}/api/reset")
    print_response(response)

def test_new_search_after_reset():
    """Test a new search after reset"""
    print_section("10. New Search After Reset")
    response = requests.post(
        f"{BASE_URL}/api/search",
        json={
            "query": "I need a Python developer for backend work",
            "reset_conversation": False
        }
    )
    print_response(response)

def main():
    """Run all tests"""
    print("\n" + "🚀 "*25)
    print("  PROMETHEUS RECRUITMENT API - TEST SUITE")
    print("🚀 "*25)
    
    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/api/health", timeout=2)
        if response.status_code != 200:
            print("\n❌ Error: Server is not responding correctly")
            return
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to server")
        print(f"   Make sure the server is running at {BASE_URL}")
        print("   Start the server with: python main.py")
        return
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return
    
    print("\n✅ Server is running!")
    
    # Run all tests
    try:
        test_health_check()
        test_root()
        test_progressive_search()
        test_conversation_state()
        test_match_score()
        test_job_description()
        test_reset()
        test_new_search_after_reset()
        
        print("\n" + "="*70)
        print("  ✅ All tests completed successfully!")
        print("="*70)
        print("\n📚 View interactive documentation at:")
        print(f"   Swagger UI: {BASE_URL}/docs")
        print(f"   ReDoc:      {BASE_URL}/redoc")
        print()
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {e}")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")

if __name__ == "__main__":
    main()
