from flask import Flask, request, jsonify
from flask_cors import CORS
import string
from chat_responses import commands, responses  # Import commands and responses
import analysis

app = Flask(__name__)
CORS(app)

def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

def get_chatbot_response(user_input):
    try:
        # Find the index of the user_input in commands
        index = commands.index(user_input.lower())
        # Return the corresponding response
        return responses[index]
    except ValueError:
        # If the command is not found
        return "Sorry, I don't understand that command."

def recognize_cmd(audio_data):
    command = remove_punctuation(audio_data.strip().lower())
    return get_chatbot_response(command)

@app.route('/', methods=['POST'])
def handle_voice_recognition():
    if request.method == 'POST':
        audio_data = request.data  # Access the raw audio data
        response = recognize_cmd(audio_data.decode('utf-8'))
        return jsonify({'command': audio_data.decode('utf-8'), 'response': response})

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    print(data)
    ticker = data.get('ticker')
    recommendations = analysis.recommend_stocks(ticker)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
