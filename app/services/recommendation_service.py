import math
from app.models import User
from app.models import UserPreference

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def recommend_users(current_user_id):
    current_user_pref = UserPreference.query.filter_by(user_id=current_user_id).first()
    current_user = User.query.get(current_user_id)

    if not current_user_pref or not current_user:
        return []

    max_distance_km = current_user_pref.max_distance_km

    potential_users = User.query.filter(
        User.id != current_user_id,
        User.age.between(current_user_pref.min_age, current_user_pref.max_age),
        User.gender.in_(current_user_pref.interested_in_genders.split(',')) 
    ).all()

    recommended_users = []
    for user in potential_users:
        if user.location_x is not None and user.location_y is not None:
            distance = calculate_distance(
                current_user.location_x, current_user.location_y,
                user.location_x, user.location_y
            )
            if max_distance_km is None or distance <= max_distance_km:
                recommended_users.append(user)

    return recommended_users
