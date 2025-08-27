# FastAPI CRUD Application

A simple CRUD (Create, Read, Update, Delete) application built with FastAPI, MongoDB, and Pydantic.

## Features

- ✅ Full CRUD operations for users
- ✅ Data validation with Pydantic
- ✅ MongoDB integration
- ✅ Environment variable configuration
- ✅ Automatic API documentation with Swagger
- ✅ Input validation and error handling
- ✅ Clean project structure

## Project Structure

```
Assignment1/
├── app/
│   ├── main.py              # FastAPI application
│   ├── database/
│   │   └── connection.py    # MongoDB connection
│   ├── models/
│   │   └── user.py         # Pydantic models
│   └── routes/
│       └── users.py        # User CRUD routes
├── .env                     # Environment variables
├── .env.example            # Environment variables template
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

## Development

To extend this application:

1. Add new models in `app/models/`
2. Create new routes in `app/routes/`
3. Include new routers in `app/main.py`
4. Update database operations in respective route files