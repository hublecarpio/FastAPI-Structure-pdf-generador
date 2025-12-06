# PDF Template Rendering API

## Overview
A FastAPI-based PDF template rendering service that allows users to:
- Upload HTML templates with Jinja2 syntax
- Render those templates with dynamic data to generate PDFs
- Manage API keys for secure programmatic access
- Track render logs for analytics

## Project Structure
```
app/
├── core/           # Core configurations and utilities
│   ├── config.py   # Settings and environment configuration
│   ├── database.py # SQLAlchemy database connection
│   ├── s3.py       # S3/local storage integration
│   └── security.py # JWT token and password utilities
├── models/         # SQLAlchemy ORM models
│   ├── user.py     # User accounts
│   ├── template.py # HTML templates
│   ├── apikey.py   # API keys for authentication
│   └── renderlog.py# Render operation logs
├── schemas/        # Pydantic request/response schemas
│   ├── user.py     # User schemas
│   ├── template.py # Template schemas
│   ├── apikey.py   # API key schemas
│   └── render.py   # Render request/response schemas
├── services/       # Business logic layer
│   ├── auth_service.py     # Authentication logic
│   ├── template_service.py # Template CRUD operations
│   ├── render_service.py   # PDF rendering logic
│   ├── apikey_service.py   # API key management
│   └── log_service.py      # Render logging
├── routes/         # API endpoint definitions
│   ├── auth.py     # /auth/* endpoints
│   ├── me.py       # /me endpoint
│   ├── templates.py# /templates/* endpoints
│   ├── render.py   # /render/* endpoints
│   └── apikeys.py  # /apikeys/* endpoints
├── utils/          # Helper utilities
│   ├── jinja_engine.py # Jinja2 template processing
│   └── pdf_engine.py   # WeasyPrint PDF generation
└── main.py         # FastAPI application entry point
```

## API Endpoints

### Authentication
- `POST /auth/register` - Create a new user account
- `POST /auth/login` - Login and get JWT tokens
- `POST /auth/refresh` - Refresh access token

### User
- `GET /me` - Get current user info

### API Keys
- `POST /apikeys/create` - Generate new API key
- `GET /apikeys` - List all API keys
- `DELETE /apikeys/{id}` - Revoke an API key

### Templates
- `POST /templates` - Upload a new HTML template
- `GET /templates` - List all templates
- `GET /templates/{id}` - Get template details
- `PUT /templates/{id}` - Update a template
- `DELETE /templates/{id}` - Delete a template

### Rendering
- `POST /render/{template_id}` - Render template to PDF with provided data

## Technologies
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Database (via Replit)
- **WeasyPrint** - HTML to PDF conversion
- **Jinja2** - Template engine
- **JWT** - Token-based authentication
- **Boto3** - S3 storage (optional, falls back to local)

## Environment Variables
- `DATABASE_URL` - PostgreSQL connection string (auto-configured by Replit)
- `SESSION_SECRET` - Secret key for JWT tokens
- `AWS_ACCESS_KEY_ID` - (Optional) S3 access key
- `AWS_SECRET_ACCESS_KEY` - (Optional) S3 secret key
- `AWS_REGION` - (Optional) AWS region, defaults to us-east-1
- `S3_BUCKET` - (Optional) S3 bucket name, defaults to pdf-templates

## Running the Project
The API server runs automatically via the configured workflow:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

Access the API documentation at `/docs` (Swagger UI) or `/redoc`.

## Recent Changes
- 2024-12-06: Initial project setup with complete API implementation
  - User registration and JWT authentication
  - Template CRUD with S3/local storage
  - PDF rendering with Jinja2 + WeasyPrint
  - API key management
  - Render logging
