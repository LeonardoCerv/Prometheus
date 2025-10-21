# 🚀 Quick Start Guide - Prometheus Recruitment API

Get the API server up and running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation & Startup

### Option 1: Using the Startup Script (Recommended)

#### Windows:
```bash
cd api_server
start_server.bat
```

#### Linux/Mac:
```bash
cd api_server
chmod +x start_server.sh
./start_server.sh
```

The script will:
1. Check Python installation
2. Create a virtual environment
3. Install dependencies
4. Start the server

### Option 2: Manual Setup

1. **Navigate to the api_server directory:**
   ```bash
   cd api_server
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server:**
   ```bash
   python main.py
   ```

## Verify Installation

Once the server starts, you should see:
```
🚀 Starting Prometheus Recruitment API Server
============================================================
📍 Server will be available at: http://localhost:8000
📚 API Documentation: http://localhost:8000/docs
📖 ReDoc Documentation: http://localhost:8000/redoc
============================================================
```

Visit http://localhost:8000 to confirm the server is running.

## Test the API

### Option 1: Using the Test Script
```bash
python test_api.py
```

### Option 2: Using the Example Client
```bash
python example_client.py
```

### Option 3: Using Postman
1. Import `Prometheus_API.postman_collection.json` into Postman
2. Run the requests in order

### Option 4: Using curl

**Search for candidates:**
```bash
curl -X POST "http://localhost:8000/api/search" ^
  -H "Content-Type: application/json" ^
  -d "{\"query\": \"I need a React developer\", \"reset_conversation\": false}"
```

**Health check:**
```bash
curl http://localhost:8000/api/health
```

## Interactive Documentation

Visit these URLs while the server is running:

- **Swagger UI:** http://localhost:8000/docs
  - Interactive API documentation
  - Test endpoints directly in the browser
  
- **ReDoc:** http://localhost:8000/redoc
  - Clean, readable API documentation

## Common Workflows

### 1. Progressive Search
```bash
# Initial search
curl -X POST http://localhost:8000/api/search -H "Content-Type: application/json" -d "{\"query\": \"I need a React developer\"}"

# Refine to senior
curl -X POST http://localhost:8000/api/search -H "Content-Type: application/json" -d "{\"query\": \"only senior level\"}"

# Add Next.js requirement
curl -X POST http://localhost:8000/api/search -H "Content-Type: application/json" -d "{\"query\": \"with Next.js\"}"
```

### 2. Generate Job Description
```bash
# After doing searches, generate a job description
curl -X POST http://localhost:8000/api/job-description
```

### 3. Calculate Match Score
```bash
curl -X POST http://localhost:8000/api/match-score \
  -H "Content-Type: application/json" \
  -d "{\"candidate_name\": \"Maria Garcia\", \"job_title\": \"Senior React Developer\"}"
```

## Troubleshooting

### Server won't start
- Ensure Python 3.8+ is installed: `python --version`
- Check if port 8000 is available
- Install dependencies: `pip install -r requirements.txt`

### Import errors
- Make sure you're in the correct directory
- The `conversation_agent` folder should be in the parent directory

### Connection refused
- Verify the server is running
- Check the server URL is http://localhost:8000
- Look for error messages in the server console

## Next Steps

1. **Explore the API:** Visit http://localhost:8000/docs
2. **Run examples:** `python example_client.py`
3. **Read the full README:** Check `README.md` for detailed documentation
4. **Integrate with your app:** Use the `PrometheusClient` class from `example_client.py`

## Stop the Server

Press `Ctrl+C` in the terminal where the server is running.

## Support

For issues or questions:
1. Check the full README.md
2. Review the API documentation at /docs
3. Run the test suite: `python test_api.py`

---

Happy recruiting! 🎯
