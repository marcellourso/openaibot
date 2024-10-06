from flask import Flask, request, jsonify, render_template, session
import openai
import os

app = Flask(__name__)

# Configura la chiave segreta per le sessioni
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key')

# Ottieni la chiave API di OpenAI dalle variabili d'ambiente
openai.api_key = os.getenv('OPENAI_API_KEY')

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

    # Richiesta al modello GPT-4 tramite OpenAI API
    try:
        response = openai.chat.completions.create(
            model="gpt-4",  # Assicurati che il modello sia corretto
            messages=session['chat_history']
        )
        bot_reply = response.choices[0].message.content  # Corretto l'accesso alla risposta
        session['chat_history'].append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        bot_reply = f"Errore: {str(e)}"

    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)

