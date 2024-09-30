import json
import uuid
from flask import Blueprint, request, Response
from app.services.openai_service import get_openai_response
import datetime

chat_blueprint = Blueprint('chat', __name__)
def save_messages_to_json(conversation_id, user_message, assistant_response):
    log_entry = {
        "user_message": user_message,
        "assistant_response": assistant_response,
        'timestamp': datetime.datetime.now().isoformat()
    }

    try:
        try:
            with open('data/chat_log.json', 'r') as f:
                chat_log = json.load(f)
        except FileNotFoundError:
            chat_log = {}

        if conversation_id not in chat_log:
            chat_log[conversation_id] = []

        chat_log[conversation_id].append(log_entry)


        with open('data/chat_log.json', 'w') as f:
            json.dump(chat_log, f, indent=4)

    except Exception as e:
        print("Error saving messages:", e)

@chat_blueprint.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    conversation_id = data.get('conversation_id', str(uuid.uuid4()))

    if not user_message:
        return Response("Message is required", status=400)

    def generate():
        assistant_response = ""
        try:
            for chunk in get_openai_response(user_message):
                yield f"data: {chunk}\n\n"
                assistant_response += chunk

            save_messages_to_json(conversation_id, user_message, assistant_response)

            yield f"data: {{\"conversation_id\": \"{conversation_id}\"}}\n\n"

        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"

    return Response(generate(), content_type='text/event-stream')

@chat_blueprint.route('/chat', methods=['GET'])
def get_conversations():
    try:
        with open('data/chat_log.json', 'r') as f:
            chat_log = json.load(f)

            # format response
            formatted_chat_log = []
            for conversation_id, messages in chat_log.items():
                formatted_chat_log.append({
                    "conversation_id": conversation_id,
                    "messages": messages,
                })

        return Response(json.dumps(formatted_chat_log), content_type='application/json')
    except Exception as e:
        return Response("Error loading conversations", status=500)