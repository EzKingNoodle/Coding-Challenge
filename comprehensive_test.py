import requests
import json
import time

BASE_URL = 'http://localhost:5000/api/users'

def print_response(test_name, response):
    print(f"{test_name}:", response.status_code, end=' ')
    try:
        print(response.json() if response.text else 'No content')
    except:
        print(response.text if response.text else 'No content')

def test_user_management():
    print("\n=== Testing User Registration ===")
    # Test 1: Valid registration
    register_data = {
        'username': 'testuser8',
        'email': 'test8@example.com',
        'password': 'testpass123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    response = requests.post(f'{BASE_URL}/register', json=register_data)
    print_response('1. Valid Registration', response)
    
    # Test 2: Duplicate username
    response = requests.post(f'{BASE_URL}/register', json=register_data)
    print_response('2. Duplicate Username', response)
    
    # Test 3: Invalid email format
    invalid_email_data = register_data.copy()
    invalid_email_data['email'] = 'invalid-email'
    invalid_email_data['username'] = 'testuser9'
    response = requests.post(f'{BASE_URL}/register', json=invalid_email_data)
    print_response('3. Invalid Email', response)
    
    # Test 4: Short password
    short_pass_data = register_data.copy()
    short_pass_data['password'] = '123'
    short_pass_data['username'] = 'testuser10'
    short_pass_data['email'] = 'test10@example.com'
    response = requests.post(f'{BASE_URL}/register', json=short_pass_data)
    print_response('4. Short Password', response)

    print("\n=== Testing Authentication ===")
    # Test 5: Valid login
    login_data = {
        'username': 'testuser8',
        'password': 'testpass123'
    }
    response = requests.post(f'{BASE_URL}/login', json=login_data)
    print_response('5. Valid Login', response)
    token = response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    # Test 6: Invalid password
    invalid_login = {
        'username': 'testuser8',
        'password': 'wrongpass'
    }
    response = requests.post(f'{BASE_URL}/login', json=invalid_login)
    print_response('6. Invalid Password', response)

    # Test 7: Non-existent user
    nonexistent_login = {
        'username': 'nonexistent',
        'password': 'testpass123'
    }
    response = requests.post(f'{BASE_URL}/login', json=nonexistent_login)
    print_response('7. Non-existent User', response)

    print("\n=== Testing Protected Endpoints ===")
    # Test 8: Get current user (with valid token)
    response = requests.get(f'{BASE_URL}/me', headers=headers)
    print_response('8. Get Current User', response)
    user_id = response.json()['id']

    # Test 9: Get current user (without token)
    response = requests.get(f'{BASE_URL}/me')
    print_response('9. Get User Without Token', response)

    # Test 10: Update user profile
    update_data = {
        'first_name': 'Updated',
        'last_name': 'Name',
        'email': 'updated8@example.com'
    }
    response = requests.put(f'{BASE_URL}/{user_id}', headers=headers, json=update_data)
    print_response('10. Update Profile', response)

    # Test 11: Try to update another user's profile
    response = requests.put(f'{BASE_URL}/{user_id + 1}', headers=headers, json=update_data)
    print_response('11. Update Other User', response)

    # Test 12: Update with duplicate email
    another_user_data = register_data.copy()
    another_user_data['username'] = 'testuser11'
    another_user_data['email'] = 'test11@example.com'
    requests.post(f'{BASE_URL}/register', json=another_user_data)
    
    duplicate_email_data = {'email': 'test11@example.com'}
    response = requests.put(f'{BASE_URL}/{user_id}', headers=headers, json=duplicate_email_data)
    print_response('12. Update with Duplicate Email', response)

    # Test 13: Get specific user
    response = requests.get(f'{BASE_URL}/{user_id}', headers=headers)
    print_response('13. Get Specific User', response)

    # Test 14: Get non-existent user
    response = requests.get(f'{BASE_URL}/999', headers=headers)
    print_response('14. Get Non-existent User', response)

    print("\n=== Cleanup ===")
    # Test 15: Delete user
    response = requests.delete(f'{BASE_URL}/{user_id}', headers=headers)
    print_response('15. Delete User', response)

    # Test 16: Verify deletion
    response = requests.get(f'{BASE_URL}/{user_id}', headers=headers)
    print_response('16. Verify Deletion', response)

if __name__ == '__main__':
    test_user_management() 