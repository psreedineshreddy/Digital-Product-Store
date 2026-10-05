# Digital Product Store

A full-stack digital product store built with FastAPI and React.

## Features

- User registration and login
- JWT authentication
- Product CRUD operations
- Product search and pagination
- Shopping cart
- Order management
- Stripe Checkout integration
- Stripe webhook
- Admin dashboard and reports
- Input validation and error handling
- Pytest API tests

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- SQLite
- JWT
- Stripe
- Pytest

### Frontend
- React
- Vite
- Axios
- React Router
- React Toastify
- Tailwind CSS

## Project Structure

Digital-Product-Store/
├── backend/
└── frontend/

## Run Backend

cd backend
source venv/bin/activate
uvicorn app.main:app --reload

Backend:
http://127.0.0.1:8000

Swagger:
http://127.0.0.1:8000/docs

## Run Frontend

cd frontend
npm install
npm run dev

Frontend:
http://localhost:5173

## Testing

Run backend tests:

cd backend
python -m pytest

Current result:

8 passed

## Stripe

Stripe Checkout and webhook are implemented using Stripe test-mode configuration.

Stripe keys should be stored in the .env file and should not be committed to Git.