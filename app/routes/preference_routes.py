from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db
from app.models import User, UserPreference

bp = Blueprint('prefs', __name__)

@bp.route('/preferences', methods=['PUT'])
@jwt_required()
def update_preferences():
    current_user = get_jwt_identity()
    user_id = current_user['user_id']

    data = request.get_json()

    user_preference = UserPreference.query.filter_by(user_id=user_id).first()

    if not user_preference:
        user_preference = UserPreference(
            user_id=user_id,
            min_age=data.get('min_age'),
            max_age=data.get('max_age'),
            max_distance_km=data.get('max_distance_km'),
            interests=data.get('interests'),
            interested_in_confessions=data.get('interested_in_confessions'),
            not_interested_in_confessions=data.get('not_interested_in_confessions'),
            interested_in_genders=data.get('interested_in_genders', "")
        )
        db.session.add(user_preference)
    else:
        user_preference.min_age = data.get('min_age', user_preference.min_age)
        user_preference.max_age = data.get('max_age', user_preference.max_age)
        user_preference.max_distance_km = data.get('max_distance_km', user_preference.max_distance_km)
        user_preference.interests = data.get('interests', user_preference.interests)
        user_preference.interested_in_confessions = data.get('interested_in_confessions', user_preference.interested_in_confessions)
        user_preference.not_interested_in_confessions = data.get('not_interested_in_confessions', user_preference.not_interested_in_confessions)
        user_preference.interested_in_genders = data.get('interested_in_genders', user_preference.interested_in_genders)

    db.session.commit()

    return jsonify({"message": "Preferences updated successfully"}), 200
