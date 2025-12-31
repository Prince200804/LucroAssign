# 🛒 LucroAssign - E-Commerce Analytics Platform

<p align="center">
  <img src="https://img.shields.io/badge/Django-5.2.9-green?style=for-the-badge&logo=django" alt="Django">
  <img src="https://img.shields.io/badge/Vue.js-3.x-4FC08D?style=for-the-badge&logo=vue.js" alt="Vue.js">
  <img src="https://img.shields.io/badge/Vuetify-3.x-1867C0?style=for-the-badge&logo=vuetify" alt="Vuetify">
  <img src="https://img.shields.io/badge/Stripe-Payment-635BFF?style=for-the-badge&logo=stripe" alt="Stripe">
  <img src="https://img.shields.io/badge/Railway-Deployed-0B0D0E?style=for-the-badge&logo=railway" alt="Railway">
  <img src="https://img.shields.io/badge/Vercel-Deployed-000000?style=for-the-badge&logo=vercel" alt="Vercel">
</p>

A **full-stack e-commerce platform** with comprehensive analytics, Stripe payment integration, and admin dashboard. Built with Django REST Framework and Vue.js 3.

---

## 🌐 Live Demo

| Service | URL |
|---------|-----|
| 🖥️ **Frontend** | [https://lucro-assign.vercel.app](https://lucro-assign.vercel.app) |
| ⚙️ **Backend API** | [https://web-production-fc881.up.railway.app/api/](https://web-production-fc881.up.railway.app/api/) |
| 💚 **Health Check** | [https://web-production-fc881.up.railway.app/health/](https://web-production-fc881.up.railway.app/health/) |

### 🔐 Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| **Admin** | `admin@example.com` | `admin123` |
| **User** | `user@example.com` | `user123` |

---

## ✨ Features

### 🛍️ Customer Features
- **Product Browsing** - Browse products with filtering by category, price range, and search
- **Shopping Cart** - Add, update, remove items with real-time price calculation
- **User Authentication** - Register, login, logout with JWT tokens
- **Secure Checkout** - Stripe payment integration with credit card processing
- **Order History** - View past orders with status tracking
- **Anonymous Shopping** - Browse and add to cart without registration

### 👨‍💼 Admin Features
- **Admin Dashboard** - Comprehensive analytics with charts and statistics
- **Product Management** - Full CRUD operations for products and categories
- **Order Management** - View, update status, and manage all orders
- **User Analytics** - Track user behavior, interactions, and patterns
- **Data Export** - Download reports in Excel (XLSX) and PDF formats:
  - 📊 Orders Export (Excel & PDF)
  - 📈 Analytics Export (Excel & PDF)
  - 📦 Products Export (Excel)

### 📊 Analytics Tracking
- Product views and interactions
- Add to cart events
- Search queries
- Daily statistics aggregation
- User behavior patterns
- Real-time dashboard updates

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Django 5.2.9** | Web framework |
| **Django REST Framework** | REST API |
| **Simple JWT** | JWT authentication |
| **Stripe Python SDK** | Payment processing |
| **SQLite** | Database (development) |
| **Gunicorn** | WSGI HTTP server |
| **WhiteNoise** | Static file serving |
| **openpyxl** | Excel file generation |
| **reportlab** | PDF generation |
| **django-cors-headers** | CORS handling |

### Frontend
| Technology | Purpose |
|------------|---------|
| **Vue.js 3** | JavaScript framework |
| **Vuetify 3** | Material Design UI |
| **Pinia** | State management |
| **Vue Router** | Client-side routing |
| **Axios** | HTTP client |
| **Stripe.js** | Payment UI elements |
| **Vite** | Build tool |

### Deployment
| Service | Purpose |
|---------|---------|
| **Railway** | Backend hosting |
| **Vercel** | Frontend hosting |
| **GitHub** | Version control |

---

## 📁 Project Structure

```
LucroAssign/
├── backend/                    # Django Backend
│   ├── core/                   # Project settings
│   │   ├── settings.py         # Django configuration
│   │   ├── urls.py             # Root URL routing
│   │   └── wsgi.py             # WSGI application
│   │
│   ├── users/                  # User management
│   │   ├── models.py           # User, AnonymousSession models
│   │   ├── views.py            # Auth endpoints
│   │   ├── serializers.py      # Data serialization
│   │   └── urls.py             # User routes
│   │
│   ├── products/               # Product catalog
│   │   ├── models.py           # Category, Product, ProductImage
│   │   ├── views.py            # Product CRUD, filtering
│   │   ├── serializers.py      # Product serialization
│   │   └── urls.py             # Product routes
│   │
│   ├── cart/                   # Shopping cart
│   │   ├── models.py           # Cart, CartItem models
│   │   ├── views.py            # Cart operations
│   │   ├── serializers.py      # Cart serialization
│   │   └── urls.py             # Cart routes
│   │
│   ├── orders/                 # Order processing
│   │   ├── models.py           # Order, OrderItem models
│   │   ├── views.py            # Checkout, Stripe, exports
│   │   ├── serializers.py      # Order serialization
│   │   └── urls.py             # Order routes
│   │
│   ├── analytics/              # Analytics tracking
│   │   ├── models.py           # ProductInteraction, DailyStats
│   │   ├── views.py            # Dashboard, analytics endpoints
│   │   ├── middleware.py       # Auto-tracking middleware
│   │   ├── serializers.py      # Analytics serialization
│   │   └── urls.py             # Analytics routes
│   │
│   ├── manage.py               # Django CLI
│   ├── requirements.txt        # Python dependencies
│   └── db.sqlite3              # SQLite database
│
├── frontend/                   # Vue.js Frontend
│   ├── src/
│   │   ├── views/              # Page components
│   │   │   ├── HomeView.vue
│   │   │   ├── ProductsView.vue
│   │   │   ├── ProductDetailView.vue
│   │   │   ├── CartView.vue
│   │   │   ├── CheckoutView.vue
│   │   │   ├── OrdersView.vue
│   │   │   ├── LoginView.vue
│   │   │   ├── RegisterView.vue
│   │   │   └── admin/
│   │   │       ├── DashboardView.vue
│   │   │       ├── ProductsView.vue
│   │   │       └── OrdersView.vue
│   │   │
│   │   ├── components/         # Reusable components
│   │   │   ├── NavBar.vue
│   │   │   └── FooterComponent.vue
│   │   │
│   │   ├── stores/             # Pinia state stores
│   │   │   ├── auth.js         # Authentication state
│   │   │   └── cart.js         # Cart state
│   │   │
│   │   ├── services/           # API services
│   │   │   └── api.js          # Axios configuration
│   │   │
│   │   ├── router/             # Vue Router
│   │   │   └── index.js        # Route definitions
│   │   │
│   │   ├── plugins/            # Vue plugins
│   │   │   └── vuetify.js      # Vuetify configuration
│   │   │
│   │   ├── App.vue             # Root component
│   │   └── main.js             # Application entry
│   │
│   ├── index.html              # HTML template
│   ├── package.json            # Node dependencies
│   ├── vite.config.js          # Vite configuration
│   └── vercel.json             # Vercel deployment config
│
├── railway.toml                # Railway configuration
├── nixpacks.toml               # Nixpacks build config
├── Procfile                    # Process definition
├── PROJECT_DOCUMENTATION.md    # Detailed code documentation
└── README.md                   # This file
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.11+**
- **Node.js 18+**
- **npm or yarn**
- **Stripe Account** (for payments)

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Prince200804/LucroAssign.git
   cd LucroAssign/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   
   Create a `.env` file in the `backend` folder:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
   STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
   FRONTEND_URL=http://localhost:5173
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Load sample data**
   ```bash
   python manage.py seed_data
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```
   
   Backend will be available at: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set environment variables**
   
   Create a `.env` file in the `frontend` folder:
   ```env
   VITE_API_URL=http://localhost:8000/api
   VITE_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```
   
   Frontend will be available at: `http://localhost:5173`

---

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/users/register/` | Register new user |
| `POST` | `/api/users/login/` | Login and get tokens |
| `POST` | `/api/users/token/refresh/` | Refresh access token |
| `GET` | `/api/users/profile/` | Get user profile |
| `POST` | `/api/users/anonymous-session/` | Create anonymous session |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/products/` | List all products |
| `GET` | `/api/products/{id}/` | Get product details |
| `GET` | `/api/products/categories/` | List all categories |
| `POST` | `/api/products/admin/products/` | Create product (admin) |
| `PUT` | `/api/products/admin/products/{id}/` | Update product (admin) |
| `DELETE` | `/api/products/admin/products/{id}/` | Delete product (admin) |

### Cart
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/cart/` | Get cart items |
| `POST` | `/api/cart/add/` | Add item to cart |
| `PUT` | `/api/cart/update/{id}/` | Update cart item quantity |
| `DELETE` | `/api/cart/remove/{id}/` | Remove item from cart |
| `DELETE` | `/api/cart/clear/` | Clear entire cart |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/orders/` | List user orders |
| `GET` | `/api/orders/{id}/` | Get order details |
| `POST` | `/api/orders/create-payment-intent/` | Create Stripe PaymentIntent |
| `POST` | `/api/orders/confirm/` | Confirm order after payment |
| `GET` | `/api/orders/admin/orders/` | List all orders (admin) |
| `PATCH` | `/api/orders/admin/orders/{id}/` | Update order status (admin) |

### Analytics (Admin Only)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/analytics/dashboard/` | Get dashboard statistics |
| `GET` | `/api/analytics/interactions/` | Get product interactions |
| `GET` | `/api/analytics/daily-stats/` | Get daily statistics |
| `POST` | `/api/analytics/track/` | Track user interaction |

### Export Endpoints (Admin Only)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/orders/admin/export/orders/excel/` | Download orders as Excel |
| `GET` | `/api/orders/admin/export/orders/pdf/` | Download orders as PDF |
| `GET` | `/api/analytics/export/excel/` | Download analytics as Excel |
| `GET` | `/api/analytics/export/pdf/` | Download analytics as PDF |
| `GET` | `/api/products/admin/export/excel/` | Download products as Excel |

### Health Check
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health/` | API health status |

---

## 💳 Stripe Integration

The application uses **Stripe PaymentIntent API** for secure payment processing.

### Test Card Numbers
| Card Number | Description |
|-------------|-------------|
| `4242 4242 4242 4242` | Successful payment |
| `4000 0000 0000 0002` | Card declined |
| `4000 0000 0000 9995` | Insufficient funds |

**Expiry:** Any future date  
**CVC:** Any 3 digits  
**ZIP:** Any 5 digits

### Payment Flow
1. User adds items to cart
2. User proceeds to checkout
3. Frontend creates PaymentIntent via backend
4. Stripe Elements collects card details
5. Frontend confirms payment with Stripe
6. Backend verifies payment and creates order

---

## 🚢 Deployment

### Backend (Railway)

1. **Create Railway account** at [railway.app](https://railway.app)

2. **Connect GitHub repository**

3. **Set environment variables** in Railway:
   ```
   SECRET_KEY=your-production-secret-key
   DEBUG=False
   STRIPE_SECRET_KEY=sk_live_or_sk_test_xxx
   STRIPE_PUBLISHABLE_KEY=pk_live_or_pk_test_xxx
   FRONTEND_URL=https://your-vercel-domain.vercel.app
   ```

4. **Configure build settings**:
   - Root Directory: `/`
   - Build Command: (handled by `nixpacks.toml`)
   - Start Command: (handled by `railway.toml`)

5. **Deploy** - Railway will automatically build and deploy

### Frontend (Vercel)

1. **Create Vercel account** at [vercel.com](https://vercel.com)

2. **Import GitHub repository**

3. **Configure project**:
   - Framework Preset: `Vite`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

4. **Set environment variables**:
   ```
   VITE_API_URL=https://your-railway-backend.up.railway.app/api
   VITE_STRIPE_PUBLISHABLE_KEY=pk_live_or_pk_test_xxx
   ```

5. **Deploy** - Vercel will automatically build and deploy

---

## 📊 Admin Dashboard

Access the admin dashboard at `/admin/dashboard` after logging in with admin credentials.

### Dashboard Features
- **Revenue Overview** - Total sales and order statistics
- **Product Performance** - Most viewed and purchased products
- **User Analytics** - Registration trends and user behavior
- **Real-time Charts** - Interactive data visualization
- **Quick Actions** - Manage products and orders

### Export Options
- **Orders Report** - Complete order history with customer details
- **Analytics Report** - User interactions and behavior patterns
- **Products Report** - Full product catalog with inventory

---

## 🔐 Authentication Flow

The application uses **JWT (JSON Web Tokens)** for authentication:

1. **Registration** - User creates account with email/password
2. **Login** - Server returns `access` and `refresh` tokens
3. **API Calls** - Access token sent in `Authorization: Bearer <token>` header
4. **Token Refresh** - When access token expires, use refresh token to get new access token
5. **Logout** - Frontend clears stored tokens

### Token Configuration
- **Access Token Lifetime:** 1 day
- **Refresh Token Lifetime:** 7 days

---

## 🧪 Sample Data

The `seed_data` management command creates:

- **Admin User:** `admin@example.com` / `admin123`
- **Regular User:** `user@example.com` / `user123`
- **Categories:** Electronics, Clothing, Books, Home & Kitchen, Sports
- **Products:** 5 sample products with images and descriptions
- **Sample Analytics:** Product interactions and daily statistics

Run seed data:
```bash
python manage.py seed_data
```

---

## 📝 Environment Variables

### Backend (.env)
| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | ✅ |
| `DEBUG` | Debug mode (True/False) | ✅ |
| `STRIPE_SECRET_KEY` | Stripe secret key | ✅ |
| `STRIPE_PUBLISHABLE_KEY` | Stripe publishable key | ✅ |
| `FRONTEND_URL` | Frontend URL for CORS | ✅ |
| `DATABASE_URL` | Database connection string | ❌ |

### Frontend (.env)
| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_API_URL` | Backend API URL | ✅ |
| `VITE_STRIPE_PUBLISHABLE_KEY` | Stripe publishable key | ✅ |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Prince200804**

- GitHub: [@Prince200804](https://github.com/Prince200804)

---

## 🙏 Acknowledgments

- [Django](https://www.djangoproject.com/) - The web framework for perfectionists with deadlines
- [Vue.js](https://vuejs.org/) - The Progressive JavaScript Framework
- [Vuetify](https://vuetifyjs.com/) - Material Design Component Framework
- [Stripe](https://stripe.com/) - Online payment processing
- [Railway](https://railway.app/) - Infrastructure platform
- [Vercel](https://vercel.com/) - Frontend cloud platform

---

<p align="center">
  Made with ❤️ by Prince200804
</p>
