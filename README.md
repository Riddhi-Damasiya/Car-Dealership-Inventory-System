# Car Dealership Inventory System

## Overview

A full-stack TDD kata submission for a car dealership inventory management system. This project demonstrates professional software engineering practices including Test-Driven Development, clean code principles, role-based access control, and responsive UI design.

**Tech Stack:**
- **Backend:** Python + FastAPI + SQLAlchemy
- **Database:** PostgreSQL
- **Frontend:** React + Tailwind CSS
- **Authentication:** JWT-based tokens
- **ORM:** SQLAlchemy (async) + Alembic for migrations

## Features

### User Features
- User registration and login with JWT authentication
- Browse available vehicles with real-time inventory
- Search and filter vehicles by make, model, category, and price range
- Purchase vehicles (decrement quantity)
- View purchase confirmation

### Admin Features
- Add new vehicles to inventory
- Update vehicle details (price, quantity, specifications)
- Delete vehicles from inventory
- Restock vehicles (increment quantity)
- View all vehicles and their quantities

### Technical Features
- Async database operations for high performance
- Role-based access control (user vs admin)
- Comprehensive test coverage (>80%)
- Responsive design (mobile, tablet, desktop)
- Clean code with SOLID principles
- Git workflow with descriptive commits
- AI co-authorship documentation

## Local Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 13+
- Docker & Docker Compose (optional)

### Backend Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Riddhi-Damasiya/Car-Dealership-Inventory-System.git
   cd Car-Dealership-Inventory-System
   ```

2. **Set up Python environment:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and secret key
   ```

4. **Start PostgreSQL (using Docker):**
   ```bash
   docker-compose up -d postgres
   ```

5. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Run backend tests:**
   ```bash
   pytest tests/ -v --cov=app
   ```

7. **Start the backend server:**
   ```bash
   uvicorn app.main:app --reload
   # Server runs on http://localhost:8000
   ```

### Frontend Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Run development server:**
   ```bash
   npm run dev
   # Server runs on http://localhost:5173
   ```

3. **Run tests:**
   ```bash
   npm run test
   npm run coverage
   ```

4. **Run E2E tests:**
   ```bash
   npm run e2e
   ```

### Using Docker Compose

```bash
docker-compose up
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
# PostgreSQL: localhost:5432
```

## API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Vehicle Endpoints (Protected Routes)
- `GET /api/vehicles` - List all vehicles (authenticated)
- `GET /api/vehicles/search` - Search vehicles with filters (authenticated)
- `POST /api/vehicles` - Add new vehicle (admin only)
- `GET /api/vehicles/{id}` - Get vehicle details (authenticated)
- `PUT /api/vehicles/{id}` - Update vehicle (admin only)
- `DELETE /api/vehicles/{id}` - Delete vehicle (admin only)
- `POST /api/vehicles/{id}/purchase` - Purchase vehicle (authenticated)
- `POST /api/vehicles/{id}/restock` - Restock vehicle (admin only)

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── dependencies.py      # DI for auth
│   │   ├── database.py          # DB setup
│   │   ├── config.py            # Configuration
│   │   └── routers/             # Route modules
│   ├── tests/                   # Test suite
│   ├── migrations/              # Alembic migrations
│   ├── requirements.txt         # Python dependencies
│   └── .env.example             # Environment template
├── frontend/
│   ├── src/
│   │   ├── pages/               # Page components
│   │   ├── components/          # Reusable components
│   │   ├── services/            # API client
│   │   ├── utils/               # Utility functions
│   │   ├── App.jsx              # Main app
│   │   └── main.jsx             # Entry point
│   ├── package.json             # Node dependencies
│   └── tailwind.config.js       # Tailwind config
├── docker-compose.yml           # Docker setup
├── README.md                    # This file
├── PROMPTS.md                   # AI usage documentation
└── CONTRIBUTING.md              # Contributing guide
```

## Test Report

### Backend Tests
```
Total Tests: [To be updated after Phase 10]
Coverage: [To be updated after Phase 10]
Status: All passing
```

### Frontend Tests
```
Total Tests: [To be updated after Phase 10]
Coverage: [To be updated after Phase 10]
Status: All passing
```

### E2E Tests
```
Total Tests: [To be updated after Phase 10]
Status: All passing
```

## Screenshots


## My AI Usage

This project extensively uses AI assistance to:
- Draft implementation code following TDD principles
- Generate test cases and edge case scenarios
- Optimize database queries and API endpoints
- Review and refactor code for SOLID principles
- Assist with documentation and commit messages

**Full AI conversation history is documented in [PROMPTS.md](./PROMPTS.md).**

Each commit where AI assistance was used includes a co-author trailer:
```
Co-authored-by: Antigravity <antigravity@users.noreply.github.com>
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development guidelines.

## License

MIT
