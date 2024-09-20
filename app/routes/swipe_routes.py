from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import db
from app.models import Match, Swipe

bp = Blueprint('swipes', __name__)

@bp.route('/swipe', methods=['POST'])
@jwt_required()
def swipe():
    # Extract the user_id from the JWT identity
    current_user = get_jwt_identity()
    current_user_id = current_user['user_id']
    
    # Get the data from the request
    data = request.get_json()
    target_user_id = data['target_user_id']
    is_like = data['is_like']  # True for like (right swipe), False for dislike (left swipe)

    existing_swipe = Swipe.query.filter_by(swiper_id=current_user_id, target_id=target_user_id).first()
    if existing_swipe:
        return jsonify({"message": "Swipe already recorded"}), 400

    new_swipe = Swipe(swiper_id=current_user_id, target_id=target_user_id, is_like=is_like)
    db.session.add(new_swipe)
    db.session.commit()

    if is_like:
        reciprocal_swipe = Swipe.query.filter_by(swiper_id=target_user_id, target_id=current_user_id, is_like=True).first()
        if reciprocal_swipe:
            new_match = Match(user1_id=current_user_id, user2_id=target_user_id)
            db.session.add(new_match)
            db.session.commit()
            return jsonify({
                "message": "It's a match!",
                "match": {
                    "user1_id": current_user_id,
                    "user2_id": target_user_id
                }
            }), 201
    return jsonify({"message": "Swipe recorded"}), 200
