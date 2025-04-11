import requests
import json

BASE_URL = 'http://localhost:5000/api/users'

def test_jwt_auth():
    # 1. Register a new user
    register_data = {
        'username': 'testuser7',
        'email': 'test7@example.com',
        'password': 'testpass123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    response = requests.post(f'{BASE_URL}/register', json=register_data)
    print('Register response:', response.status_code, response.json())
    
    if response.status_code == 201:
        user_id = response.json()['id']
        
        # 2. Login to get JWT token
        login_data = {
            'username': 'testuser7',
            'password': 'testpass123'
        }
        response = requests.post(f'{BASE_URL}/login', json=login_data)
        print('Login response:', response.status_code, response.json())
        
        if response.status_code == 200:
            token = response.json()['access_token']
            headers = {'Authorization': f'Bearer {token}'}
            
            # 3. Get current user details
            response = requests.get(f'{BASE_URL}/me', headers=headers)
            print('Get current user response:', response.status_code, response.json())
            
            # 4. Update user
            update_data = {
                'first_name': 'Updated',
                'last_name': 'Name'
            }
            response = requests.put(f'{BASE_URL}/{user_id}', headers=headers, json=update_data)
            print('Update user response:', response.status_code, response.json())
            
            # 5. Delete user
            response = requests.delete(f'{BASE_URL}/{user_id}', headers=headers)
            print('Delete user response:', response.status_code)

if __name__ == '__main__':
    test_jwt_auth() 