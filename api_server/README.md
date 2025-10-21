# Prometheus Recruitment API Server

FastAPI server that exposes the Prometheus recruitment agent functionality through REST endpoints.

## Features

- **Progressive Candidate Search**: Multi-turn conversational filtering that refines results
- **Match Score Calculation**: Semantic compatibility scoring between candidates and jobs
- **Job Description Generation**: Auto-generate job descriptions from search queries
- **Conversation State Management**: Track and reset search conversations

## Installation

1. Navigate to the api_server directory:
```bash
cd api_server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

Start the server with:
```bash
python main.py
```

The server will start at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Interactive API Docs (Swagger)**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## Endpoints

### 1. Progressive Search
**POST** `/api/search`

Search for candidates with natural language queries. Each query refines previous results.

**Request:**
```json
{
  "query": "I need a React developer",
  "reset_conversation": false
}
```

**Response:**
```json
{
  "status": "success",
  "conversation_turn": 1,
  "current_query": "I need a React developer",
  "combined_filters": {
    "skills": ["react"],
    "experience_level": "any",
    "availability": "any"
  },
  "total_candidates_searched": 20,
  "matches_found": 12,
  "matches": [...],
  "refinement_suggestion": "You have 12 matches..."
}
```

### 2. Calculate Match Score
**POST** `/api/match-score`

Calculate compatibility score between a candidate and job position.

**Request:**
```json
{
  "candidate_name": "Maria Garcia",
  "job_title": "Senior React Developer"
}
```

**Response:**
```json
{
  "status": "success",
  "candidate": "Maria Garcia",
  "job": "Senior React Developer",
  "score": 85,
  "reasoning": "Strong match based on...",
  "strengths": ["React", "TypeScript", "Node.js"],
  "gaps": ["None identified"],
  "recommendation": "Strong match - recommend interview"
}
```

### 3. Reset Search
**POST** `/api/reset`

Reset the search conversation to start fresh.

**Response:**
```json
{
  "status": "success",
  "message": "Search reset. Ready for a new candidate search."
}
```

### 4. Generate Job Description
**POST** `/api/job-description`

Generate a job description based on search conversation history.

**Response:**
```json
{
  "status": "success",
  "conversation_turns": 3,
  "queries": ["I need a React developer", "senior level", "with Next.js"],
  "required_skills": ["react", "next.js"],
  "experience_level": "senior",
  "availability": "any",
  "candidates_matching": 5
}
```

### 5. Conversation State
**GET** `/api/conversation-state`

Get current conversation state and history.

**Response:**
```json
{
  "status": "success",
  "turns": 2,
  "queries": ["I need a React developer", "only senior"],
  "candidates_remaining": 5,
  "history": [...]
}
```

### 6. Health Check
**GET** `/api/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "Prometheus Recruitment API"
}
```

## Example Usage

### Using curl:

```bash
# Search for candidates
curl -X POST "http://localhost:8000/api/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "I need a React developer", "reset_conversation": false}'

# Calculate match score
curl -X POST "http://localhost:8000/api/match-score" \
  -H "Content-Type: application/json" \
  -d '{"candidate_name": "Maria Garcia", "job_title": "Senior React Developer"}'

# Reset search
curl -X POST "http://localhost:8000/api/reset"

# Generate job description
curl -X POST "http://localhost:8000/api/job-description"

# Get conversation state
curl -X GET "http://localhost:8000/api/conversation-state"
```

### Using Python requests:

```python
import requests

# Search for candidates
response = requests.post(
    "http://localhost:8000/api/search",
    json={"query": "I need a React developer", "reset_conversation": False}
)
print(response.json())

# Refine search
response = requests.post(
    "http://localhost:8000/api/search",
    json={"query": "only senior level", "reset_conversation": False}
)
print(response.json())
```

### Using JavaScript fetch:

```javascript
// Search for candidates
const response = await fetch('http://localhost:8000/api/search', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: 'I need a React developer',
    reset_conversation: false
  })
});
const data = await response.json();
console.log(data);
```

## Progressive Search Workflow

The progressive search allows natural conversation flow:

1. **Initial Search**:
   ```json
   {"query": "I need a web developer", "reset_conversation": false}
   ```
   Result: Shows all web developers

2. **Refine to React**:
   ```json
   {"query": "only React developers", "reset_conversation": false}
   ```
   Result: Narrows to React developers (maintains web dev context)

3. **Further Refinement**:
   ```json
   {"query": "with Next.js experience", "reset_conversation": false}
   ```
   Result: Shows only React + Next.js developers

4. **Start Fresh** (when needed):
   ```json
   {"query": "I need Python developers", "reset_conversation": true}
   ```
   Result: Clears all previous filters, starts new search

## CORS Configuration

The server is configured to accept requests from any origin (`allow_origins=["*"]`). 

**For production**, update the CORS settings in `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourfrontend.com"],  # Specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Development

The server runs in reload mode by default, automatically restarting when code changes are detected.

To disable auto-reload:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --no-reload
```

## Integration with Frontend

This API is designed to work seamlessly with the Next.js frontend in the `Frontend/` directory. The endpoints provide all necessary data for the dashboard and chat interface.

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200`: Success
- `422`: Validation Error (invalid request body)
- `500`: Internal Server Error

Error responses include a `detail` field with the error message.

## License

Part of the Prometheus Recruitment System.
