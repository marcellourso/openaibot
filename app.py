from flask import Flask, request, jsonify, render_template
import openai
#from dotenv import load_dotenv
import os

#load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY')
#openai.api_key = 'sk-proj-i2WBMFDtefACtTMlTxp6T3BlbkFJO0NIUKZVp6rjmpkX38vJ'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    response = openai.chat.completions.create(
        model="gpt-4o",  # O il modello che preferisci
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    bot_reply = response.choices[0].message.content
    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
