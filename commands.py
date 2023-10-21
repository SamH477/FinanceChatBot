import voice_rec
commands = ['hello', 'who are you?', 'goodbye']
# Basic responses
responses = ['Hello! How can I help you?', 'I am a finance chatbot!', 'see ya!'
]

while True:
    cmd = voice_rec.recognize_cmd()
    print(cmd)
    for value in commands:
        index = commands.index(value)
        if (cmd == value):
            print(commands[index])
            print(responses[index])

