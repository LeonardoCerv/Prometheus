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
        
    result = progressive_search(query=query, reset_conversation=reset_conversation)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
