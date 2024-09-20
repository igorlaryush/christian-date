from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import db

from ..models import Chat, Message

bp = Blueprint('chats', __name__)

# Get all messages from a chat
@bp.route('/chats/<int:chat_id>/messages', methods=['GET'])
@jwt_required()
def get_chat_messages(chat_id):
    current_user = get_jwt_identity()
    current_user_id = current_user['user_id']

    chat = Chat.query.get_or_404(chat_id)

    if current_user_id not in [chat.user1_id, chat.user2_id]:
        return jsonify({"error": "You are not a participant of this chat"}), 403

    messages = Message.query.filter_by(chat_id=chat.id).order_by(Message.timestamp.asc()).all()

    return jsonify([{
        "id": msg.id,
        "sender_id": msg.sender_id,
        "content": msg.content,
        "timestamp": msg.timestamp
    } for msg in messages]), 200

# Create or retrieve a chat between two users
@bp.route('/chats/<int:target_user_id>', methods=['POST'])
@jwt_required()
def create_or_get_chat(target_user_id):
    current_user = get_jwt_identity()
    current_user_id = current_user['user_id']

    # Check if the chat already exists
    chat = Chat.query.filter(
        ((Chat.user1_id == current_user_id) & (Chat.user2_id == target_user_id)) |
        ((Chat.user1_id == target_user_id) & (Chat.user2_id == current_user_id))
    ).first()

    if chat is None:
        # Create a new chat
        chat = Chat(user1_id=current_user_id, user2_id=target_user_id)
        db.session.add(chat)
        db.session.commit()

    return jsonify({"chat_id": chat.id}), 200
