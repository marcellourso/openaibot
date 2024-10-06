from flask import Flask, request, jsonify, render_template, session
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

     # Se non c'è uno storico, inizializzalo
    if 'chat_history' not in session:
        session['chat_history'] = []

    # Aggiungi il messaggio dell'utente alla cronologia
    session['chat_history'].append({"role": "user", "content": user_message})

    response = openai.chat.completions.create(
        model="gpt-4o",  # O il modello che preferisci
        messages=session['chat_history']
    )
    bot_reply = response.choices[0].message.content
    session['chat_history'].append({"role": "assistant", "content": bot_reply})
    
    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
