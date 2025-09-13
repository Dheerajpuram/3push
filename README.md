# Telecom Subscription Management System

A full-stack web application for managing telecom subscriptions with separate admin and user interfaces.

## Project Structure

```
hackathonlumen/
├── backend/                 # Flask backend
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   ├── db.py               # Database configuration
│   ├── models/             # SQLAlchemy models
│   ├── routes/             # API routes
│   ├── services/           # Business logic services
│   └── utils/              # Utility functions
├── frontend/               # React frontend
│   ├── src/
│   │   ├── pages/          # React pages
│   │   ├── components/     # Reusable components
│   │   └── utils/          # API utilities
│   └── public/             # Static files
└── README.md               # This file
```

## Features

### ✅ Implemented
- User authentication (Admin/User roles)
- User registration
- Role-based navigation
- Database initialization with demo admin user
- Responsive UI with Tailwind CSS
- Complete authentication flow

### 🚧 Placeholder (Ready for Development)
- Plan management
- Subscription management
- Usage tracking
- Discount management
- Analytics dashboard
- Billing system

## Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Database Setup
1. Install MySQL
2. Create database: `telecom_subscription_db`
3. Update database URL in `backend/config.py` if needed

## Demo Credentials

- **Admin**: admin@example.com / admin123
- **User**: Register through the signup page

## Tech Stack

### Backend
- Flask
- SQLAlchemy
- MySQL
- Flask-CORS

### Frontend
- React 18
- React Router DOM
- Tailwind CSS
- Axios

## API Endpoints

### Admin
- `POST /admin/login` - Admin login
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/plans` - Manage plans
- `GET /admin/discounts` - Manage discounts
- `GET /admin/users` - Manage users
- `GET /admin/analytics` - Analytics

### User
- `POST /user/signup` - User registration
- `POST /user/login` - User login
- `GET /user/dashboard` - User dashboard
- `GET /user/subscriptions` - My subscriptions
- `GET /user/recommendations` - Plan recommendations
- `GET /user/usage` - Usage history
- `GET /user/billing` - Billing

## Database Schema

The application includes the following tables:
- **users** - User accounts and roles
- **plans** - Subscription plans
- **subscriptions** - User subscriptions
- **usage** - Data usage records
- **discounts** - Promotional discounts
- **audit_logs** - System audit trail
- **alerts** - User notifications

## Development Status

This is a complete scaffold with working authentication. All other features are implemented as placeholders ready for development.

## Next Steps

1. Implement plan management functionality
2. Add subscription management features
3. Build usage tracking system
4. Create analytics dashboard
5. Add billing and payment processing
6. Implement notification system
