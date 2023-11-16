from flask import Flask, request, jsonify
from flask_cors import CORS
import analysis

app = Flask(__name__)
CORS(app)

commands = ['hello', 'who are you', 'what is a stock', 'goodbye']
responses = [
    'Hello! How can I help you?',
    'I am a stock recommender chatbot!',
    'A stock is a share in the ownership of a company, including a claim on the company\'s earnings and assets',
    'see ya!'
]

def recognize_cmd(audio_data):
    command = audio_data  # The audio data is directly passed as the command
    for recognized_command in commands:
        index = commands.index(recognized_command)
        if recognized_command in command:
            response = responses[index]
    return response

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
