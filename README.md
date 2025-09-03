# FastAPI CRUD Application

A simple CRUD (Create, Read, Update, Delete) application built with FastAPI, MongoDB, and Pydantic.

## Features

- ✅ Full CRUD operations for users
- ✅ Data validation with Pydantic
- ✅ MongoDB integration
- ✅ Environment variable configuration
- ✅ Automatic API documentation with Swagger
- ✅ Input validation and error handling
- ✅ Clean project structure with layered architecture
- ✅ Repository pattern for data access
- ✅ Service layer for business logic
- ✅ Custom exception handling

## Project Structure

```
Python_First_Assignment/
├── app/
│   ├── main.py              # FastAPI application
│   ├── database/
│   │   └── connection.py    # MongoDB connection
│   ├── models/
│   │   ├── user.py         # User Pydantic models
│   │   └── auth_models.py  # Auth Pydantic models
│   ├── repositories/
│   │   ├── user_repository.py  # User data access layer
│   │   └── auth_repository.py  # Auth data access layer
│   ├── services/
│   │   ├── user_service.py     # User business logic
│   │   └── auth_service.py     # Auth business logic
│   ├── routes/
│   │   ├── user_route.py       # User API endpoints
│   │   └── auth_routes.py      # Auth API endpoints
│   ├── exceptions/
│   │   └── custom_exceptions.py # Custom exception classes
│   └── utils/
│       └── auth.py         # Authentication utilities
├── .env                     # Environment variables
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Clone and Setup Environment

```bash
# Copy environment variables
cp .env.example .env

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Edit `.env` file to configure your database:

```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017/
DATABASE_NAME=crud_app

# Application Configuration
APP_NAME=CRUD API
APP_VERSION=1.0.0
DEBUG=True
```

### 4. Install and Start MongoDB

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

### 5. Run the Application

```bash
cd app
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/users/` | Create a new user |
| GET | `/api/v1/users/` | Get all users |
| GET | `/api/v1/users/{user_id}` | Get user by ID |
| PUT | `/api/v1/users/{user_id}` | Update user |
| DELETE | `/api/v1/users/{user_id}` | Delete user |

### Example Usage

**Create User:**
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "email": "john@example.com",
       "age": 30
     }'
```

**Get All Users:**
```bash
curl -X GET "http://localhost:8000/api/v1/users/"
```

## Data Validation

The application includes comprehensive validation:

- **Name**: 1-100 characters, required
- **Email**: Valid email format, unique, required
- **Age**: 1-120 years, required

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `201`: Created
- `204`: No Content (for delete)
- `400`: Bad Request (validation errors)
- `404`: Not Found
- `422`: Unprocessable Entity (Pydantic validation)

## Architecture

This application follows a layered architecture pattern:

- **Routes Layer**: Handles HTTP requests and responses
- **Service Layer**: Contains business logic and validation
- **Repository Layer**: Manages data access and database operations
- **Models Layer**: Defines data structures and validation
- **Utils Layer**: Contains utility functions and helpers
- **Exceptions Layer**: Custom exception classes

## Development

To extend this application:

1. Add new models in `app/models/`
2. Create repository classes in `app/repositories/`
3. Implement business logic in `app/services/`
4. Create API endpoints in `app/routes/`
5. Include new routers in `app/main.py`
6. Add custom exceptions in `app/exceptions/`