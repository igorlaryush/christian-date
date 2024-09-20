from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import db
from app.models import User
from app.services.recommendation_service import recommend_users

from ..models import User

bp = Blueprint('user_routes', __name__)

# Get current user's profile
@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user['email']).first()

    if not user:
        return jsonify({"message": "User not found"}), 404
    
    profile = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "bio": user.bio,
        "age": user.age,
        "gender": user.gender,
        "interests": user.interests,
        "created_at": user.created_at,
        "location_x": user.location_x,
        "location_y": user.location_y
    }
    return jsonify(profile), 200

@bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user['email']).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    user.bio = data.get('bio', user.bio)
    user.age = data.get('age', user.age)
    user.gender = data.get('gender', user.gender)
    user.interests = data.get('interests', user.interests)
    
    user.location_x = data.get('location_x', user.location_x)
    user.location_y = data.get('location_y', user.location_y)

    db.session.commit()

    return jsonify({"message": "Profile updated successfully"}), 200

# Delete current user's profile
@bp.route('/profile', methods=['DELETE'])
@jwt_required()
def delete_profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user['email']).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User profile deleted successfully"}), 200

@bp.route('/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    current_user = get_jwt_identity()
    current_user_id = current_user['user_id']
    
    recommended_users = recommend_users(current_user_id)

    response = [{
        "id": user.id,
        "username": user.username,
        "age": user.age,
        "location_x": user.location_x,
        "location_y": user.location_y,
        "bio": user.bio,
        "interests": user.interests
    } for user in recommended_users]

    return jsonify(response), 200