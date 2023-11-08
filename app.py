from flask import Flask, request, render_template, jsonify
import stockpickerbeta

app = Flask(__name__, template_folder='templates')

#create two lists: one for commands and another for corresponding responses
commands = ['hello', 'who are you', 'what is a stock', 'goodbye']
responses = ['Hello! How can I help you?', 'I am a stock recommender chatbot!', 'A stock is a share in the ownership of a company, including a claim on the companys earnings and assets', 'see ya!']

def recognize_cmd(audio_data):
    command = audio_data  # The audio data is directly passed as the command
    for recognized_command in commands:
        index = commands.index(recognized_command)
        if recognized_command in command:
            response = responses[index]
    return response

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        audio_data = request.data  # Access the raw audio data
        response = recognize_cmd(audio_data.decode('utf-8'))
        return jsonify({'command': audio_data.decode('utf-8'), 'response': response})
    return render_template('index.html')

@app.route('/recommend', methods=['POST', 'GET'])
def recommend():
    ticker = request.form['ticker']  # Get the ticker from the user's input.
    recommendations = stockpickerbeta.recommend_stocks(ticker)  # Use your recommendation function here.
    return render_template('recommend.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)