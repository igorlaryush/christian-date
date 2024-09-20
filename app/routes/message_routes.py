from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import db
from app.models import Chat, Message

bp = Blueprint('messages', __name__)

@bp.route('/chats/<int:chat_id>/messages', methods=['POST'])
@jwt_required()
def send_message(chat_id):
    current_user = get_jwt_identity()
    current_user_id = current_user['user_id']

    content = request.json.get('content', '')

    chat = Chat.query.get_or_404(chat_id)

    if current_user_id not in [chat.user1_id, chat.user2_id]:
        return jsonify({"error": "You are not a participant of this chat"}), 403

    message = Message(chat_id=chat_id, sender_id=current_user_id, content=content)
    db.session.add(message)
    db.session.commit()

    return jsonify({"message": "Message sent"}), 201
