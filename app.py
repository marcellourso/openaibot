from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)


# Ottieni la chiave API di OpenAI dalle variabili d'ambiente
openai.api_key = os.getenv('OPENAI_API_KEY')

# Supponiamo che tu abbia una lista di messaggi (storico della chat)
chat_history = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I'm good, thank you! How can I assist you today?"}
]


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    # Aggiungi il messaggio dell'utente alla cronologia
    chat_history.append({"role": "user", "content": user_message})

    # Richiesta al modello GPT-4 tramite OpenAI API
    try:
        response = openai.chat.completions.create(
            model="gpt-4",  # Assicurati che il modello sia corretto
            messages=chat_history
        )
        
    bot_reply = response.choices[0].message.content  # Corretto l'accesso alla risposta
    # Aggiungi la risposta del bot alla cronologia
    chat_history.append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        bot_reply = f"Errore: {str(e)}"

    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)

