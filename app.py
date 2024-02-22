# from flask import Flask
# import os

# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return "Hello World!"

# if __name__ == '__main__':
#     port = os.environ.get('FLASK_PORT') or 8080
#     port = int(port)

#     app.run(port=port,host='0.0.0.0')


from flask import Flask, request, render_template, jsonify
import google.generativeai as palm

app = Flask(__name__)

# Configure the API key
API_KEY = "AIzaSyBgv0a3DuNlGQy6zxarbWHiVJsUIZhy4Bc"
palm.configure(api_key=API_KEY)

@app.route('/ride')
def chat():
    return render_template('ride.html')

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/get_response')
def get_response():
    user_message = request.args.get('message')
    conversation = chat_with_palm(user_message)
    bot_response = conversation[-1]['content'] if conversation else "An error occurred."

    return jsonify({"botMessage": bot_response})

def chat_with_palm(prompt):
    examples = [
        ('Hello', 'Hi there, how can I assist you today?'),
        ('I want to make a know more about health', 'Eat well, sleep regularly, and brush always.')
    ]

    conversation = []
    if prompt.lower() == "exit":
        return conversation
# context='Speak like a Doctor and a texi driver', examples=examples
    response = palm.chat(messages=prompt, temperature=1 )
    for message in response.messages:
        conversation.append({'author': message['author'], 'content': message['content']})

    return conversation

if __name__ == '__main__':
    app.run(debug=True)
