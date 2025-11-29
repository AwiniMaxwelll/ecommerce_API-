🛒 E-Commerce Backend API
A high-performance, scalable backend system built with Django REST Framework that powers modern e-commerce applications with secure authentication, efficient product management, and seamless order processing.

🚀 Features
🔐 Authentication & Users
JWT-based user authentication

User registration and profile management

Secure password validation

Role-based permissions

🏪 Product Management
Complete CRUD operations for products and categories

Advanced filtering, sorting, and search

Product images and reviews

Inventory management with stock tracking

Featured products with rating-based selection

🛍️ Order System
Complete order lifecycle management

Shopping cart functionality

Multiple payment method support

Order status tracking (Pending → Processing → Shipped → Delivered)

Automatic inventory updates

📊 Advanced Features
Pagination and efficient data retrieval

Database indexing for optimal performance

Comprehensive API documentation with Swagger

CORS enabled for frontend integration

PostgreSQL-optimized queries

🛠️ Tech Stack
Backend Framework: Django 4.2 & Django REST Framework

Database: PostgreSQL (with SQLite for development)

Authentication: JWT (Simple JWT)

API Documentation: Swagger/OpenAPI (drf-yasg)

Filtering: Django Filter

Image Handling: Pillow

CORS: django-cors-headers

📁 Project Structure
text
ecommerce_backend/
├── backend/                 # Django project settings
├── apps/
│   ├── users/              # Authentication & user management
│   ├── products/           # Product catalog & reviews
│   └── orders/             # Order processing & payments
├── requirements.txt        # Project dependencies
├── docker-compose.yml      # Container orchestration
└── manage.py              # Django management script
🚀 Quick Start
Prerequisites
Python 3.10+

PostgreSQL (or SQLite for development)

pip (Python package manager)

Installation
Clone the repository

bash
git clone https://github.com/yourusername/ecommerce-backend.git
cd ecommerce-backend
Create virtual environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Configure environment variables

bash
cp .env.example .env
# Edit .env with your database credentials and secret key
Run migrations

bash
python manage.py makemigrations
python manage.py migrate
Create superuser

bash
python manage.py createsuperuser
Run development server

bash
python manage.py runserver
The API will be available at http://localhost:8000/

🗄️ Database Setup
PostgreSQL (Production)
bash
# Update settings.py with your PostgreSQL credentials
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
SQLite (Development - Default)
SQLite is configured by default for easy development setup.

📚 API Documentation
Once the server is running, access the interactive API documentation:

Swagger UI: http://localhost:8000/swagger/

ReDoc: http://localhost:8000/redoc/

🔌 API Endpoints
Authentication
POST /api/auth/register/ - User registration

POST /api/auth/login/ - User login (JWT tokens)

GET /api/auth/profile/ - User profile management

Products
GET /api/products/products/ - List all products

GET /api/products/products/featured/ - Featured products

GET /api/products/products/{slug}/ - Product details

POST /api/products/products/{slug}/add_review/ - Add product review

GET /api/products/categories/ - Product categories

Orders
GET /api/orders/orders/ - User's order history

POST /api/orders/orders/ - Create new order

GET /api/orders/orders/{id}/ - Order details

POST /api/orders/orders/{id}/cancel/ - Cancel order

POST /api/orders/orders/{id}/create_payment/ - Process payment

🐳 Docker Deployment
Using Docker Compose
bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs

# Stop services
docker-compose down
Services
Web API: http://localhost:8000

PostgreSQL: localhost:5432

PgAdmin: http://localhost:5050 (Database management)

🔧 Configuration
Environment Variables
Create a .env file in the project root:

env
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=ecommerce
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
Key Settings
DEBUG: Set to False in production

SECRET_KEY: Use a secure random key in production

CORS_ALLOWED_ORIGINS: Configure for your frontend domains

🧪 Testing
Run the test suite:

bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.users
python manage.py test apps.products
python manage.py test apps.orders
📊 Database Schema
https://docs/erd-diagram.png

The system uses a normalized database schema with:

Users: Custom user model with email authentication

Products: Catalog with categories, images, and reviews

Orders: Complete order lifecycle with payments

Relationships: Proper foreign key constraints and indexes

🚀 Deployment
Production Checklist
Set DEBUG=False

Generate new SECRET_KEY

Configure production database

Set up static files serving

Configure allowed hosts

Set up SSL/HTTPS

Configure CORS for production domains

Set up logging and monitoring

Using Gunicorn
bash
pip install gunicorn
gunicorn backend.wsgi:application --bind 0.0.0.0:8000
🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🛣️ Roadmap
Redis caching integration

Elasticsearch for advanced product search

Payment gateway integration (Stripe, PayPal)

Email notifications

Admin dashboard enhancements

Mobile app support

Analytics and reporting

Multi-vendor support

📞 Support
For support, email support@yourapp.com or create an issue in the repository.

🙏 Acknowledgments
Django REST Framework team

PostgreSQL community

All contributors and testers

Built with ❤️ using Django REST Framework
