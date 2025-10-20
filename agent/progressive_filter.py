"""
Progressive Candidate Filtration System
Allows for multi-turn conversations that progressively narrow down candidates
"""

from typing import List, Dict, Any, Optional
import json
import os


class ProgressiveFilter:
    """
    Manages progressive filtering of candidates through multi-turn conversations.
    Each query refines the previous results, showing best matches at each stage.
    """
    
    def __init__(self):
        self.conversation_history: List[Dict[str, Any]] = []
        self.current_candidates: List[Dict[str, Any]] = []
        self.all_candidates: List[Dict[str, Any]] = self._load_candidates()
        
    def _load_candidates(self) -> List[Dict[str, Any]]:
        """Load mock candidates from JSON file"""
        try:
            with open(os.path.join(os.path.dirname(__file__), 'mock_candidates.json'), 'r') as f:
                data = json.load(f)
                return data['candidates']
        except Exception as e:
            print(f"Warning: Could not load mock data: {e}")
            return []
    
    def _calculate_skill_match(self, candidate_skills: List[str], required_skills: List[str]) -> Dict[str, Any]:
        """Calculate detailed skill match with scoring"""
        candidate_skills_lower = [s.lower() for s in candidate_skills]
        required_skills_lower = [s.lower() for s in required_skills]
        
        # Direct matches
        direct_matches = [s for s in required_skills_lower if s in candidate_skills_lower]
        
        # Transferable skills mapping
        transferable_map = {
            'react': ['vue.js', 'angular', 'next.js'],
            'vue.js': ['react', 'angular'],
            'angular': ['react', 'vue.js'],
            'next.js': ['react'],
            'node.js': ['express', 'nestjs', 'fastapi'],
            'python': ['django', 'fastapi'],
            'javascript': ['typescript'],
            'typescript': ['javascript']
        }
        
        # Find transferable skills
        transferable_matches = []
        transferable_score = 0
        for required in required_skills_lower:
            if required not in direct_matches:
                for candidate_skill in candidate_skills_lower:
                    if candidate_skill in transferable_map.get(required, []):
                        transferable_matches.append({
                            'required': required,
                            'has': candidate_skill
                        })
                        transferable_score += 15
                        break
        
        # Calculate score
        if required_skills_lower:
            direct_score = (len(direct_matches) / len(required_skills_lower)) * 100
            total_score = min(100, direct_score + transferable_score)
        else:
            total_score = 100
            
        return {
            'score': round(total_score, 1),
            'direct_matches': direct_matches,
            'transferable_matches': transferable_matches,
            'missing_skills': [s for s in required_skills_lower if s not in direct_matches and 
                              not any(t['required'] == s for t in transferable_matches)]
        }
    
    def _extract_requirements_from_query(self, query: str) -> Dict[str, Any]:
        """
        Extract requirements from natural language query
        Uses simple keyword matching - in production would use Gemini
        """
        query_lower = query.lower()
        
        # Extract experience level
        experience_level = "any"
        if any(word in query_lower for word in ["senior", "sr", "lead", "principal"]):
            experience_level = "senior"
        elif any(word in query_lower for word in ["junior", "jr", "entry", "entry-level"]):
            experience_level = "junior"
        elif any(word in query_lower for word in ["mid", "mid-level", "intermediate"]):
            experience_level = "mid"
        
        # Extract availability
        availability = "any"
        if any(word in query_lower for word in ["full-time", "full time", "fulltime"]):
            availability = "full-time"
        elif any(word in query_lower for word in ["freelance", "contractor"]):
            availability = "freelance"
        elif any(word in query_lower for word in ["part-time", "part time", "parttime"]):
            availability = "part-time"
        elif "contract" in query_lower:
            availability = "contract"
        
        # Extract skills (comprehensive list)
        skill_keywords = {
            'react': ['react', 'reactjs', 'react.js'],
            'next.js': ['next', 'nextjs', 'next.js'],
            'vue.js': ['vue', 'vuejs', 'vue.js'],
            'angular': ['angular'],
            'typescript': ['typescript', 'ts'],
            'javascript': ['javascript', 'js'],
            'node.js': ['node', 'nodejs', 'node.js'],
            'python': ['python'],
            'django': ['django'],
            'fastapi': ['fastapi', 'fast api'],
            'express': ['express', 'expressjs'],
            'graphql': ['graphql', 'graph ql'],
            'rest': ['rest', 'restful', 'rest api'],
            'mongodb': ['mongodb', 'mongo'],
            'postgresql': ['postgresql', 'postgres', 'psql'],
            'aws': ['aws', 'amazon web services'],
            'docker': ['docker', 'containers'],
            'tailwind': ['tailwind', 'tailwindcss'],
            'css': ['css', 'styling'],
            'html': ['html'],
            'redux': ['redux'],
            'firebase': ['firebase'],
            'testing': ['test', 'testing', 'jest', 'cypress', 'unit test']
        }
        
        detected_skills = []
        for skill, keywords in skill_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                detected_skills.append(skill)
        
        # Infer role-based skills
        if 'web developer' in query_lower or 'frontend' in query_lower:
            if not detected_skills:
                detected_skills = ['javascript', 'html', 'css']
        elif 'backend' in query_lower:
            if not detected_skills:
                detected_skills = ['python', 'node.js']
        elif 'full stack' in query_lower or 'fullstack' in query_lower:
            if not detected_skills:
                detected_skills = ['javascript', 'react', 'node.js']
        
        return {
            'skills': detected_skills,
            'experience_level': experience_level,
            'availability': availability,
            'raw_query': query
        }
    
    def filter_candidates(self, query: str, min_score: float = 60.0) -> Dict[str, Any]:
        """
        Progressive filtering: applies new query on top of existing filters
        """
        # Extract requirements from new query
        new_requirements = self._extract_requirements_from_query(query)
        
        # Add to conversation history
        self.conversation_history.append({
            'query': query,
            'requirements': new_requirements
        })
        
        # Combine all requirements from conversation history
        all_skills = []
        final_experience_level = "any"
        final_availability = "any"
        
        for turn in self.conversation_history:
            reqs = turn['requirements']
            all_skills.extend(reqs['skills'])
            
            # More specific filters override general ones
            if reqs['experience_level'] != "any":
                final_experience_level = reqs['experience_level']
            if reqs['availability'] != "any":
                final_availability = reqs['availability']
        
        # Remove duplicates from skills
        all_skills = list(set(all_skills))
        
        # Start with current candidates or all if first query
        candidates_to_filter = self.current_candidates if self.current_candidates else self.all_candidates
        
        # Filter candidates
        matches = []
        for candidate in candidates_to_filter:
            # Check experience level
            if final_experience_level != "any" and candidate["experience_level"] != final_experience_level:
                continue
            
            # Check availability
            if final_availability != "any" and candidate["availability"] != final_availability:
                continue
            
            # Calculate skill match
            if all_skills:
                skill_analysis = self._calculate_skill_match(candidate["skills"], all_skills)
                
                # Only include if meets minimum score
                if skill_analysis['score'] >= min_score:
                    matches.append({
                        "candidate_id": candidate["id"],
                        "name": candidate["name"],
                        "email": candidate["email"],
                        "phone": candidate["phone"],
                        "score": skill_analysis['score'],
                        "skills": candidate["skills"],
                        "experience_years": candidate["total_years"],
                        "experience_level": candidate["experience_level"],
                        "availability": candidate["availability"],
                        "location": candidate["location"],
                        "matched_skills": skill_analysis['direct_matches'],
                        "transferable_skills": skill_analysis['transferable_matches'],
                        "missing_skills": skill_analysis['missing_skills'],
                        "reasoning": self._generate_reasoning(candidate, skill_analysis, all_skills),
                        "hourly_rate": candidate.get("hourly_rate"),
                        "salary_expectation": candidate.get("salary_expectation")
                    })
            else:
                # No skills specified, use base score
                matches.append({
                    "candidate_id": candidate["id"],
                    "name": candidate["name"],
                    "email": candidate["email"],
                    "phone": candidate["phone"],
                    "score": 100,
                    "skills": candidate["skills"],
                    "experience_years": candidate["total_years"],
                    "experience_level": candidate["experience_level"],
                    "availability": candidate["availability"],
                    "location": candidate["location"],
                    "matched_skills": candidate["skills"][:3],
                    "transferable_skills": [],
                    "missing_skills": [],
                    "reasoning": f"{candidate['name']} has {candidate['total_years']} years of experience.",
                    "hourly_rate": candidate.get("hourly_rate"),
                    "salary_expectation": candidate.get("salary_expectation")
                })
        
        # Sort by score (descending)
        matches.sort(key=lambda x: x["score"], reverse=True)
        
        # Update current candidates for next iteration
        self.current_candidates = [
            c for c in self.all_candidates 
            if c["id"] in [m["candidate_id"] for m in matches]
        ]
        
        return {
            "status": "success",
            "conversation_turn": len(self.conversation_history),
            "current_query": query,
            "combined_filters": {
                "skills": all_skills,
                "experience_level": final_experience_level,
                "availability": final_availability
            },
            "total_candidates_searched": len(candidates_to_filter),
            "matches_found": len(matches),
            "matches": matches[:10],  # Return top 10
            "refinement_suggestion": self._suggest_refinement(matches, all_skills)
        }
    
    def _generate_reasoning(self, candidate: Dict[str, Any], skill_analysis: Dict[str, Any], 
                           required_skills: List[str]) -> str:
        """Generate human-readable reasoning for match"""
        reasoning_parts = []
        
        # Direct matches
        if skill_analysis['direct_matches']:
            reasoning_parts.append(
                f"Has {len(skill_analysis['direct_matches'])}/{len(required_skills)} required skills: "
                f"{', '.join(skill_analysis['direct_matches'][:3])}"
            )
        
        # Transferable skills
        if skill_analysis['transferable_matches']:
            examples = skill_analysis['transferable_matches'][:2]
            transferable_text = ', '.join([f"{t['has']} (similar to {t['required']})" for t in examples])
            reasoning_parts.append(f"Transferable skills: {transferable_text}")
        
        # Experience
        reasoning_parts.append(
            f"{candidate['total_years']} years of experience as {candidate['experience_level']}"
        )
        
        # Availability
        reasoning_parts.append(f"Available for {candidate['availability']}")
        
        return ". ".join(reasoning_parts) + "."
    
    def _suggest_refinement(self, matches: List[Dict[str, Any]], current_skills: List[str]) -> str:
        """Suggest how to further refine the search"""
        if not matches:
            return "Try broadening your search by removing some requirements or considering transferable skills."
        
        if len(matches) > 5:
            # Suggest being more specific
            common_skills = {}
            for match in matches:
                for skill in match['skills']:
                    skill_lower = skill.lower()
                    if skill_lower not in current_skills:
                        common_skills[skill_lower] = common_skills.get(skill_lower, 0) + 1
            
            if common_skills:
                top_skills = sorted(common_skills.items(), key=lambda x: x[1], reverse=True)[:3]
                skill_list = ', '.join([s[0] for s in top_skills])
                return f"You have {len(matches)} matches. Consider adding specific requirements like: {skill_list}"
            
            return f"You have {len(matches)} strong matches. Consider specifying experience level or particular frameworks."
        
        return f"Found {len(matches)} excellent match{'es' if len(matches) > 1 else ''}!"
    
    def reset(self):
        """Reset the filter to start a new conversation"""
        self.conversation_history = []
        self.current_candidates = []
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get summary of the filtering conversation"""
        return {
            "turns": len(self.conversation_history),
            "queries": [turn['query'] for turn in self.conversation_history],
            "candidates_remaining": len(self.current_candidates),
            "history": self.conversation_history
        }
