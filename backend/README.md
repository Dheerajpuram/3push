# Telecom Subscription Management - Backend

Flask backend for the Telecom Subscription Management System.

## Features

- User authentication (Admin/User roles)
- User registration
- Database models for all subscription management entities
- RESTful API endpoints
- MySQL database integration
- Audit logging

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up MySQL database:
- Create a database named `telecom_subscription_db`
- Update the database URL in `config.py` if needed

3. Run the application:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Admin Routes
- `POST /admin/login` - Admin login
- `GET /admin/dashboard` - Admin dashboard (placeholder)
- `GET /admin/plans` - Manage plans (placeholder)
- `GET /admin/discounts` - Manage discounts (placeholder)
- `GET /admin/users` - Manage users (placeholder)
- `GET /admin/analytics` - Analytics (placeholder)

### User Routes
- `POST /user/signup` - User registration
- `POST /user/login` - User login
- `GET /user/dashboard` - User dashboard (placeholder)
- `GET /user/subscriptions` - My subscriptions (placeholder)
- `GET /user/recommendations` - Plan recommendations (placeholder)
- `GET /user/usage` - Usage history (placeholder)
- `GET /user/billing` - Billing (placeholder)

## Demo Credentials

- **Admin**: admin@example.com / admin123
- **User**: Register through the signup endpoint

## Database Schema

The application automatically creates the following tables:
- users
- plans
- subscriptions
- usage
- discounts
- audit_logs
- alerts
