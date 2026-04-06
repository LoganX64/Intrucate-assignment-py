from flask import Flask, request, jsonify
import asyncio

from db import init_db
from services.openai_service import get_ai_response
from services.history_service import save_to_history   

app = Flask(__name__)
mongo = init_db(app)

# Single Prompt Endpoint
@app.route('/api/prompt', methods=['POST'])
def single_prompt():
    data = request.get_json()
    if not data or 'userInput' not in data:
        return jsonify({"error": "UserInput required"}), 400
    
    userInput = data['userInput']

    try:
        aiResponse = asyncio.run(get_ai_response(userInput))

        save_to_history(userInput, aiResponse, is_batch=False)

        return jsonify({
            "userInput": userInput,
            "response": aiResponse
        })

    except Exception as e:
        print(f"Error in single_prompt: {e}")
        return jsonify({"error": str(e)}), 500

# Batch Prompt Endpoint
@app.route('/api/batch_prompt', methods=['POST'])
def batch_prompt():
    data = request.get_json()

    if not data or 'userInputs' not in data or not isinstance(data['userInputs'], list):
        return jsonify({"error": "User Inputs required"}), 400
        
    inputs = data['userInputs']

    try:
        async def process_batch():
            tasks = [get_ai_response(userInput) for userInput in inputs]
            return await asyncio.gather(*tasks,return_exceptions=True)

        responses = asyncio.run(process_batch())

        result = []
        for user_input, resp in zip(inputs, responses):
            if isinstance(resp, Exception):
                answer = f"Error: {str(resp)}"
            else:
                answer = resp

            result.append({
                "userInput": user_input,
                "response": answer
            })

            save_to_history(user_input, answer, is_batch=True)
        return jsonify({"responses": result})
    
    except Exception as e:
        print(f"Error in batch_prompt: {e}")
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    print("\nServer running on http://127.0.0.1:5001")
    app.run(debug=True, port=5001)