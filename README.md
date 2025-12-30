# 🛒 E-Commerce Product Interaction Analytics Platform

[![Django](https://img.shields.io/badge/Django-5.2.9-green.svg)](https://www.djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-brightgreen.svg)](https://vuejs.org/)
[![Vuetify](https://img.shields.io/badge/Vuetify-3.x-blue.svg)](https://vuetifyjs.com/)
[![Stripe](https://img.shields.io/badge/Stripe-Payment-blueviolet.svg)](https://stripe.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A full-stack e-commerce application with **advanced product interaction analytics**, **Stripe payment integration**, and **comprehensive admin reporting** built with Django REST Framework (backend) and Vue.js 3 with Vuetify (frontend).

---

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack](#️-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [API Endpoints](#-api-endpoints)
- [Stripe Payment Testing](#-stripe-payment-testing)
- [Admin Export Features](#-admin-export-features)
- [Screenshots](#-screenshots)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🌟 Features

### 🛍️ Customer Features
| Feature | Description |
|---------|-------------|
| **Product Browsing** | Browse products by category with search and filter capabilities |
| **Product Details** | View detailed product information with specifications |
| **Shopping Cart** | Add/remove products, update quantities with real-time updates |
| **Secure Checkout** | Complete purchases with **Stripe Payment Gateway** |
| **Order Management** | View order history and track order status |
| **User Authentication** | Register, login, and profile management with JWT tokens |

### 📊 Admin Features
| Feature | Description |
|---------|-------------|
| **Analytics Dashboard** | Comprehensive overview with KPI cards and interactive charts |
| **Product Analytics** | Detailed interaction tracking (views, cart additions, purchases) |
| **Most Viewed Products** | Bar charts showing top viewed products |
| **Most Purchased Products** | Sales distribution with doughnut charts |
| **Viewed But Not Purchased** | Identify products with high views but low conversions |
| **Cart Abandonment Analysis** | Track cart abandonment rates |
| **Time-based Trends** | Line graphs showing engagement over time |
| **Category Distribution** | Pie charts for category-wise analytics |
| **Export Reports** | Export data as **Excel (.xlsx)** or **PDF** |
| **Product Management** | Full CRUD operations for products |
| **Order Management** | View, filter, and update order status |

### 💳 Payment Integration
- **Stripe Payment Gateway**: Secure payment processing with PCI compliance
- **Test Mode Support**: Easy testing with Stripe test cards
- **Payment Intent API**: Modern Stripe integration with SCA compliance
- **Real-time Payment Status**: Instant payment confirmation

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.10+ | Programming Language |
| Django | 5.2.9 | Web Framework |
| Django REST Framework | 3.15+ | RESTful API |
| Simple JWT | 5.3+ | JWT Authentication |
| **Stripe** | 14.0+ | Payment Processing |
| SQLite/PostgreSQL | - | Database |
| **openpyxl** | 3.1+ | Excel Generation |
| **ReportLab** | 4.0+ | PDF Generation |
| Pillow | 10.0+ | Image Processing |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| Vue.js | 3.x | JavaScript Framework |
| Vuetify | 3.x | Material Design UI |
| Pinia | 2.x | State Management |
| Vue Router | 4.x | Client-side Routing |
| Chart.js | 4.x | Data Visualization |
| **Stripe.js** | Latest | Payment UI Elements |
| Axios | 1.x | HTTP Client |
| Vite | 5.x | Build Tool |

---

## 📁 Project Structure

```
LucroAssign/
├── 📂 backend/
│   ├── 📂 core/               # Django settings & Stripe configuration
│   │   ├── settings.py        # Main settings with Stripe keys
│   │   ├── urls.py            # Root URL configuration
│   │   └── wsgi.py
│   ├── 📂 users/              # User authentication & profiles
│   │   ├── models.py          # Custom User model
│   │   ├── serializers.py     # User serializers
│   │   └── views.py           # Auth views (register, login)
│   ├── 📂 products/           # Product catalog management
│   │   ├── models.py          # Product & Category models
│   │   └── views.py           # Product CRUD views
│   ├── 📂 cart/               # Shopping cart functionality
│   │   ├── models.py          # Cart & CartItem models
│   │   └── views.py           # Cart operations
│   ├── 📂 orders/             # Order processing & Stripe payments
│   │   ├── models.py          # Order model with Stripe fields
│   │   ├── views.py           # Stripe PaymentIntent & Export views
│   │   └── urls.py            # Order & export endpoints
│   ├── 📂 analytics/          # Product interaction analytics
│   │   ├── models.py          # Interaction tracking model
│   │   ├── middleware.py      # Auto-tracking middleware
│   │   └── views.py           # Analytics API views
│   ├── requirements.txt       # Python dependencies
│   └── manage.py
│
├── 📂 frontend/
│   ├── 📂 src/
│   │   ├── 📂 components/     # Reusable Vue components
│   │   ├── 📂 views/          # Page components
│   │   │   ├── 📂 admin/      # Admin dashboard views
│   │   │   │   ├── AnalyticsView.vue
│   │   │   │   └── OrdersManageView.vue
│   │   │   ├── CheckoutView.vue   # Stripe checkout page
│   │   │   └── ...
│   │   ├── 📂 stores/         # Pinia state stores
│   │   ├── 📂 router/         # Vue Router configuration
│   │   ├── 📂 services/       # API services (axios)
│   │   └── 📂 plugins/        # Vuetify plugin
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
├── .gitignore
└── README.md
```

---

## 🚀 Installation

### Prerequisites
- **Python** 3.10 or higher
- **Node.js** 18 or higher
- **npm** or **yarn**
- **Git**

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Prince200804/LucroAssign.git
cd LucroAssign
```

### 2️⃣ Backend Setup

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# For Command Prompt use:
# .\venv\Scripts\activate.bat

# For Linux/Mac use:
# source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser

# Seed sample data (optional)
python manage.py seed_data

# Start the Django development server
python manage.py runserver
```

Backend will be available at: **http://localhost:8000**

### 3️⃣ Frontend Setup

```powershell
# Open a new terminal
cd frontend

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

Frontend will be available at: **http://localhost:5173**

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-super-secret-key-here

# Database (optional - defaults to SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# Stripe Configuration (REQUIRED for payments)
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key
STRIPE_SECRET_KEY=sk_test_your_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

### Getting Stripe API Keys

1. Go to [Stripe Dashboard](https://dashboard.stripe.com/)
2. Create an account or log in
3. Navigate to **Developers** → **API Keys**
4. Copy your **Publishable key** and **Secret key**
5. For webhooks, go to **Developers** → **Webhooks**

---

## 🔑 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/register/` | User registration |
| POST | `/api/users/login/` | User login (returns JWT tokens) |
| POST | `/api/users/token/refresh/` | Refresh access token |
| GET | `/api/users/me/` | Get current user profile |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | List all products |
| GET | `/api/products/<slug>/` | Get product details |
| GET | `/api/products/categories/` | List categories |
| GET | `/api/products/categories/<slug>/` | Get category products |

### Cart
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/cart/` | Get user's cart |
| POST | `/api/cart/add/` | Add item to cart |
| PATCH | `/api/cart/items/<id>/` | Update cart item |
| DELETE | `/api/cart/items/<id>/` | Remove cart item |

### Orders & Payments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/orders/` | List user's orders |
| POST | `/api/orders/` | Create new order |
| GET | `/api/orders/<id>/` | Get order details |
| POST | `/api/orders/stripe/create-payment-intent/` | Create Stripe PaymentIntent |

### Admin Export Endpoints 📥
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/orders/admin/export/orders/excel/` | Export all orders to Excel |
| GET | `/api/orders/admin/export/orders/pdf/` | Export all orders to PDF |
| GET | `/api/orders/admin/export/analytics/excel/` | Export analytics to Excel |
| GET | `/api/orders/admin/export/analytics/pdf/` | Export analytics to PDF |
| GET | `/api/orders/admin/export/products/excel/` | Export products to Excel |

### Analytics (Admin only)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/analytics/overview/` | Dashboard overview |
| GET | `/api/analytics/trends/` | Engagement trends |
| GET | `/api/analytics/most-viewed/` | Most viewed products |
| GET | `/api/analytics/most-purchased/` | Most purchased products |
| GET | `/api/analytics/viewed-not-purchased/` | Products viewed but not purchased |
| GET | `/api/analytics/cart-abandonment/` | Cart abandonment data |
| GET | `/api/analytics/category-distribution/` | Category distribution |

---

## 💳 Stripe Payment Testing

### Test Card Numbers

Use these test card numbers for testing payments:

| Card Number | Description |
|-------------|-------------|
| `4242 4242 4242 4242` | Successful payment |
| `4000 0000 0000 3220` | 3D Secure authentication |
| `4000 0000 0000 9995` | Declined payment |

**For all test cards:**
- **Expiry Date**: Any future date (e.g., 12/34)
- **CVC**: Any 3 digits (e.g., 123)
- **ZIP**: Any 5 digits (e.g., 12345)

### Payment Flow

1. User adds products to cart
2. User proceeds to checkout
3. User enters shipping information
4. Stripe Payment Element appears
5. User enters card details
6. Payment is processed via Stripe PaymentIntent API
7. Order is created upon successful payment

---

## 📥 Admin Export Features

### Available Export Formats

| Data Type | Excel (.xlsx) | PDF |
|-----------|---------------|-----|
| Orders | ✅ | ✅ |
| Analytics | ✅ | ✅ |
| Products | ✅ | - |

### How to Export

1. Log in as an **Admin** user
2. Navigate to the **Admin Dashboard**
3. Go to **Orders** or **Analytics** section
4. Click the **Export** dropdown button
5. Select **Excel** or **PDF** format
6. File will be downloaded automatically

### Export Contents

**Orders Export includes:**
- Order ID, Date, Customer Info
- Products, Quantities, Prices
- Payment Status, Payment Method
- Shipping Address
- Total Amount

**Analytics Export includes:**
- Total Views, Cart Additions, Purchases
- Conversion Rates
- Top Products
- Category Distribution
- Time-based Trends

---

## 📸 Screenshots

### Customer Interface
- **Home Page**: Product catalog with category filters
- **Product Details**: Detailed product view with add to cart
- **Shopping Cart**: Cart management with quantity updates
- **Checkout**: Stripe payment integration

### Admin Dashboard
- **Analytics Overview**: KPI cards with key metrics
- **Charts**: Interactive Chart.js visualizations
- **Order Management**: Order listing with status updates
- **Export Options**: One-click export buttons

---

## 🚀 Deployment

### Frontend Deployment (Vercel)

1. **Push to GitHub** (if not already done)

2. **Connect to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Select the `frontend` folder as root directory

3. **Configure Build Settings:**
   ```
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

4. **Add Environment Variables:**
   ```
   VITE_API_URL=https://your-backend-url.com/api
   VITE_STRIPE_PUBLISHABLE_KEY=pk_test_your_key
   ```

### Backend Deployment Options

**Option 1: Railway**
- Connect GitHub repository
- Add PostgreSQL database
- Set environment variables
- Deploy!

**Option 2: Render**
- Create new Web Service
- Connect GitHub repository
- Set build command: `pip install -r requirements.txt`
- Set start command: `gunicorn core.wsgi:application`

**Option 3: DigitalOcean App Platform**
- Similar to Render setup

### Production Checklist

- [ ] Set `DEBUG=False` in Django settings
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure Stripe production keys
- [ ] Set up proper CORS origins
- [ ] Enable HTTPS
- [ ] Set up static file serving (WhiteNoise)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
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

- [Django Documentation](https://docs.djangoproject.com/)
- [Vue.js Documentation](https://vuejs.org/)
- [Vuetify Documentation](https://vuetifyjs.com/)
- [Stripe Documentation](https://stripe.com/docs)
- [Chart.js Documentation](https://www.chartjs.org/)

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/Prince200804">Prince200804</a>
</p>
