from flask import Flask, request, render_template, jsonify
import google.generativeai as palm

app = Flask(__name__)

# Configure the API key (if necessary)
API_KEY = "AIzaSyBgv0a3DuNlGQy6zxarbWHiVJsUIZhy4Bc"
if API_KEY:
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

    # Ensure API key is set if using palm.chat (replace with your API key)
    if API_KEY:
        response = palm.chat(messages=prompt, temperature=1.0)
    else:
        print("Warning: Missing API key for palm.chat. Response may be inaccurate.")
        return examples  # Replace with a suitable fallback response

    for message in response.messages:
        conversation.append({'author': message['author'], 'content': message['content']})

    return conversation

if __name__ == '__main__':
    app.run(debug=True)
