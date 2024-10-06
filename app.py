from flask import Flask, request, jsonify, render_template
import openai
from dotenv import load_dotenv
import os



load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY')

conversations = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_chat', methods=['POST'])
def start_chat():
    # Inizializza una nuova cronologia per la conversazione
    conversation_id = "default_conversation"
    conversations[conversation_id] = [ {"role": "system", "content": "Sei un assistente molto utile."}]
    return jsonify({"conversation_id": conversation_id})



@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    conversation_id = data.get('conversation_id')

    # Se non esiste una cronologia per questo ID, restituisci un errore
    if conversation_id not in conversations:
        return jsonify({'error': 'Conversazione non trovata'}), 404
    
    chat_history = conversations[conversation_id]

    # Aggiungi il messaggio dell'utente alla cronologia
    chat_history.append({"role": "user", "content": user_message})

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",  # O il modello che preferisci
            messages = chat_history
        )
        bot_reply = response.choices[0].message.content
        
        # Aggiungi la risposta del bot alla cronologia
        chat_history.append({"role": "assistant", "content": bot_reply})
    
    except Exception as e:
        bot_reply = f"Errore: {str(e)}"
    
    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)


