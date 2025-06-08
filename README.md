# FastAPI MongoDB API

This is a FastAPI application that connects to MongoDB and provides an API endpoint to fetch data from the "generic" collection.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

The server will start at `http://localhost:8000`

## API Endpoints

- `GET /`: Welcome message
- `GET /generic`: Fetch all items from the generic collection

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation at: `http://localhost:8000/docs`
- ReDoc documentation at: `http://localhost:8000/redoc` 