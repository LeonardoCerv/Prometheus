from flask import Flask, request, jsonify
from flask_cors import CORS
from conversation_agent.my_agent.agent import progressive_search

app = Flask(__name__)
CORS(app)

@app.route('/api/agent/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query')
    reset_conversation = data.get('reset_conversation', False)
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
        
    # Call the progressive search function directly
    result = progressive_search(query=query, reset_conversation=reset_conversation)
    print(f"Server received result from agent: {type(result)}")
    print(f"Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
    print(f"Main response preview: {result.get('main_response', '')[:200] if isinstance(result, dict) else 'N/A'}...")
    print(f"Profiles count: {len(result.get('profiles', [])) if isinstance(result, dict) else 'N/A'}")
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
