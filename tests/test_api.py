import pytest
import requests

# Base URL for the API
BASE_URL = 'http://127.0.0.1:5000'

# Data for registration
user1 = {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "password123"
}

user2 = {
    "username": "shara_conor",
    "email": "shara_conor@example.com",
    "password": "password456"
}

# Data for profile update
profile_data_user1 = {
    "bio": "I love hiking.",
    "age": 30,
    "gender": "Female",
    "interests": "Coding",
    "location_x": 40.7128,
    "location_y": -74.0060
}

profile_data_user2 = {
    "bio": "I love traveling and hiking.",
    "age": 30,
    "gender": "Male",
    "interests": "Hiking, Traveling, Coding",
    "location_x": 44.7128,
    "location_y": -76.0060
}

# Initialize global variables for tokens
auth_token_user1 = None
auth_token_user2 = None

# Register two users
def test_register_users():
    response = requests.post(f'{BASE_URL}/auth/register', json=user1)
    assert response.status_code == 201
    assert response.json().get('message') == 'User registered successfully'

    response = requests.post(f'{BASE_URL}/auth/register', json=user2)
    assert response.status_code == 201
    assert response.json().get('message') == 'User registered successfully'

# Login as user 1 and get token
def test_login_user1():
    response = requests.post(f'{BASE_URL}/auth/login', json={
        "email": user1['email'],
        "password": user1['password']
    })
    assert response.status_code == 200
    global auth_token_user1
    auth_token_user1 = response.json().get('access_token')
    assert auth_token_user1 is not None

# Login as user 2 and get token
def test_login_user2():
    response = requests.post(f'{BASE_URL}/auth/login', json={
        "email": user2['email'],
        "password": user2['password']
    })
    assert response.status_code == 200
    global auth_token_user2
    auth_token_user2 = response.json().get('access_token')
    assert auth_token_user2 is not None

# Update profile for user 1
def test_update_profile_user1():
    headers = {
        'Authorization': f'Bearer {auth_token_user1}'
    }
    response = requests.put(f'{BASE_URL}/user_routes/profile', json=profile_data_user1, headers=headers)
    assert response.status_code == 200
    assert response.json().get('message') == 'Profile updated successfully'

# Get profile of user 1
def test_get_profile_user1():
    headers = {
        'Authorization': f'Bearer {auth_token_user1}'
    }
    response = requests.get(f'{BASE_URL}/user_routes/profile', headers=headers)
    assert response.status_code == 200
    profile = response.json()
    assert profile['age'] == profile_data_user1['age']
    assert profile['bio'] == profile_data_user1['bio']
    assert profile['gender'] == profile_data_user1['gender']
    assert profile['interests'] == profile_data_user1['interests']
    assert profile['location_x'] == profile_data_user1['location_x']
    assert profile['location_y'] == profile_data_user1['location_y']
    assert profile['email'] == user1['email']
    assert profile['username'] == user1['username']

# Update profile for user 2
def test_update_profile_user2():
    headers = {
        'Authorization': f'Bearer {auth_token_user2}'
    }
    response = requests.put(f'{BASE_URL}/user_routes/profile', json=profile_data_user2, headers=headers)
    assert response.status_code == 200
    assert response.json().get('message') == 'Profile updated successfully'

# Swipe by user 2 on user 1
def test_swipe():
    headers = {
        'Authorization': f'Bearer {auth_token_user2}'
    }
    response = requests.post(f'{BASE_URL}/swipe/swipe', json={
        "target_user_id": 1,
        "is_like": 1
    }, headers=headers)
    assert response.status_code == 200
    assert response.json().get('message') == 'Swipe recorded'

# Create chat between user 1 and user 2
def test_create_chat():
    headers = {
        'Authorization': f'Bearer {auth_token_user1}'
    }
    response = requests.post(f'{BASE_URL}/chats/chats/2', headers=headers)
    assert response.status_code == 200
    chat_id = response.json().get('chat_id')
    assert chat_id is not None
    global chat_id_global
    chat_id_global = chat_id

# Send a message in the chat
def test_send_message():
    headers = {
        'Authorization': f'Bearer {auth_token_user1}'
    }
    response = requests.post(f'{BASE_URL}/messages/chats/{chat_id_global}/messages', json={
        "content": "Hello, this is a new message!"
    }, headers=headers)
    assert response.status_code == 201
    assert response.json().get('message') == 'Message sent'

# Get messages from the chat
def test_get_messages():
    headers = {
        'Authorization': f'Bearer {auth_token_user2}'
    }
    response = requests.get(f'{BASE_URL}/chats/chats/{chat_id_global}/messages', headers=headers)
    assert response.status_code == 200
    messages = response.json()
    assert len(messages) > 0
    assert messages[0]['content'] == "Hello, this is a new message!"
