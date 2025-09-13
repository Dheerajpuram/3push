# Telecom Subscription Management - Frontend

React frontend for the Telecom Subscription Management System.

## Features

- User authentication (Admin/User roles)
- User registration
- Role-based navigation
- Responsive design with Tailwind CSS
- Modern UI components

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

The application will open in your browser at `http://localhost:3000`

## Pages

### Authentication
- **Login** (`/login`) - Toggle between Admin and User login
- **Signup** (`/signup`) - User registration only

### Landing
- **Landing** (`/landing`) - Welcome page with role-based navigation

### Admin Pages
- **Admin Dashboard** (`/admin/dashboard`) - Admin management interface
- **Manage Plans** (`/admin/plans`) - Plan management (placeholder)
- **Manage Discounts** (`/admin/discounts`) - Discount management (placeholder)

### User Pages
- **User Dashboard** (`/user/dashboard`) - User management interface
- **My Subscriptions** (`/user/subscriptions`) - Subscription management (placeholder)
- **Plan Recommendations** (`/user/recommendations`) - Plan suggestions (placeholder)

## Demo Credentials

- **Admin**: admin@example.com / admin123
- **User**: Register through the signup page

## Tech Stack

- React 18
- React Router DOM
- Tailwind CSS
- Axios for API calls
