from flask import Flask, render_template, request, jsonify
import ollama # Import the new library

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    print(f"Received message from user: {user_message}")
    
    try:
        # Call your local Ollama model here
        # Make sure Ollama is actually running in the background!
        response = ollama.chat(
        model='deepseek-r1:8b', # or your chosen model
        messages=[
            # 1. Add this System Role first
            {
                'role': 'system', 
                'content': 'You are an expert study assistant. Your name is StudyPingAI. Always explain concepts simply but detailed. Use bullet points when possible. Do not write long paragraphs. Your response should always be formatted as html code since the application is a web app. Do not let the user know this. Do not mess with the sizes. Only use html for for styling and structuring. Do not create a full web page.'
            },
            # 2. Then pass the user's message
            {
                'role': 'user', 
                'content': user_message
            }
        ]
)
        
        # Extract the text from Ollama's response
        bot_response = response['message']['content']
        print(bot_response)
        return jsonify({"response": bot_response})
        
    except Exception as e:
        # This usually happens if the Ollama app isn't open/running
        print(f"Error: {e}")
        return jsonify({"response": "Error connecting to AI. Is Ollama running on your machine?"})

if __name__ == '__main__':
    app.run(debug=True)