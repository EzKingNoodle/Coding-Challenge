# User Management API Microservice

A robust user management microservice built with Flask, PostgreSQL, and Docker.

## Features

- User registration and authentication
- JWT-based authentication
- CRUD operations for user management
- PostgreSQL database
- Docker containerization
- Data validation and error handling

## Prerequisites

- Docker
- Docker Compose

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd user-management-api
```

2. Create a `.env` file in the root directory with the following content:
```
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:postgres@db:5432/user_management
JWT_SECRET_KEY=your-super-secret-key-change-in-production
```

3. Build and start the containers:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/users/register` - Register a new user
- `POST /api/users/login` - Login and get JWT token

### User Management
- `GET /api/users/me` - Get current user details
- `GET /api/users/<user_id>` - Get user details by ID
- `PUT /api/users/<user_id>` - Update user details
- `DELETE /api/users/<user_id>` - Delete a user

## Ready-to-Use Commands

### 1. Register a New User
```bash
curl -X POST http://localhost:5000/api/users/register -H "Content-Type: application/json" -d "{\"username\": \"testuser1\", \"email\": \"test1@example.com\", \"password\": \"testpass123\", \"first_name\": \"Test\", \"last_name\": \"User\"}"
```

### 2. Login and Get Token
```bash
curl -X POST http://localhost:5000/api/users/login -H "Content-Type: application/json" -d "{\"username\": \"testuser1\", \"password\": \"testpass123\"}"
```
- Save the `access_token` from the response for use in other commands

### 3. Get Current User Info
```bash
curl -X GET http://localhost:5000/api/users/me -H "Authorization: Bearer YOUR_TOKEN_HERE"
```
- Replace `YOUR_TOKEN_HERE` with the token from login

### 4. Get Specific User
```bash
curl -X GET http://localhost:5000/api/users/1 -H "Authorization: Bearer YOUR_TOKEN_HERE"
```
- Replace `1` with the user ID
- Replace `YOUR_TOKEN_HERE` with your token

### 5. Update User Information
```bash
curl -X PUT http://localhost:5000/api/users/1 -H "Authorization: Bearer YOUR_TOKEN_HERE" -H "Content-Type: application/json" -d "{\"first_name\": \"Updated\", \"last_name\": \"Name\", \"email\": \"updated@example.com\"}"
```
- Replace `1` with the user ID
- Replace `YOUR_TOKEN_HERE` with your token
- Modify the JSON data as needed

### 6. Delete User
```bash
curl -X DELETE http://localhost:5000/api/users/1 -H "Authorization: Bearer YOUR_TOKEN_HERE"
```
- Replace `1` with the user ID
- Replace `YOUR_TOKEN_HERE` with your token

### 7. Update Password
```bash
curl -X PUT http://localhost:5000/api/users/1 -H "Authorization: Bearer YOUR_TOKEN_HERE" -H "Content-Type: application/json" -d "{\"password\": \"newpassword123\"}"
```
- Replace `1` with the user ID
- Replace `YOUR_TOKEN_HERE` with your token
- Replace `newpassword123` with your new password

### 8. Update Username
```bash
curl -X PUT http://localhost:5000/api/users/1 -H "Authorization: Bearer YOUR_TOKEN_HERE" -H "Content-Type: application/json" -d "{\"username\": \"newusername\"}"
```
- Replace `1` with the user ID
- Replace `YOUR_TOKEN_HERE` with your token
- Replace `newusername` with your new username

## API Documentation

### Register User
```http
POST /api/users/register
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password",
    "first_name": "John",
    "last_name": "Doe"
}
```

### Login
```http
POST /api/users/login
Content-Type: application/json

{
    "username": "john_doe",
    "password": "secure_password"
}
```

### Update User
```http
PUT /api/users/<user_id>
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}
```

## Development

To run the application in development mode:

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
flask run
```

## Testing

To run tests:
```bash
python -m pytest
```

## License

MIT 