# E-Commerce Product Interaction Analytics Platform

## Project Overview
A full-stack e-commerce platform with advanced user interaction analytics featuring:
- Django REST Framework backend with PostgreSQL
- Vue.js frontend with modern UI/UX
- Comprehensive interaction tracking and analytics dashboard

## Tech Stack
- **Backend**: Django 5.x, Django REST Framework, PostgreSQL
- **Frontend**: Vue.js 3, Vuetify 3, Chart.js, Pinia
- **Authentication**: JWT tokens with session-based anonymous tracking

## Project Structure
```
LucroAssign/
├── backend/           # Django REST Framework API
│   ├── core/          # Project settings
│   ├── products/      # Product management
│   ├── users/         # User authentication
│   ├── cart/          # Shopping cart
│   ├── orders/        # Order processing
│   ├── analytics/     # Interaction tracking & analytics
│   └── manage.py
├── frontend/          # Vue.js application
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── stores/
│   │   └── router/
│   └── package.json
└── README.md
```

## Setup Instructions
1. Backend: `cd backend && pip install -r requirements.txt && python manage.py migrate`
2. Frontend: `cd frontend && npm install && npm run dev`

## Completed Steps
- [x] Project structure created
- [x] Backend Django REST Framework setup
- [x] Frontend Vue.js setup
- [x] User authentication system
- [x] Product management
- [x] Cart functionality
- [x] Order processing
- [x] Analytics tracking
- [x] Admin dashboard with charts
