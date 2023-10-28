from flask import Flask, request, jsonify, render_template
import speech_recognition as sr

app = Flask(__name__)

# Voice recognition function
def recognize_cmd(audio_data):
    command = audio_data  # The audio data is directly passed as the command
    response = "Command not Recognized"
    for recognized_command in commands:
        index = commands.index(recognized_command)
        if recognized_command in command:
            response = responses[index]
    return response

commands = ['hello', 'who are you?', 'goodbye']
responses = ['Hello! How can I help you?', 'I am a finance chatbot!', 'see ya!']

@app.route('/', methods=['POST', 'GET'])
def recognition():
    if request.method == 'POST':
        audio_data = request.data  # Access the raw audio data
        response = recognize_cmd(audio_data.decode('utf-8'))
        return jsonify({'command': audio_data.decode('utf-8'), 'response': response})
    return render_template('audio_capture.html')

if __name__ == '__main__':
    app.run(debug=True)
