# PayIt - Agricultural Marketplace API

A RESTful API marketplace connecting farmers with buyers, built with FastAPI, MySQL, and Docker.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Authentication](#authentication)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

---

## 🌾 Overview

PayIt is an agricultural marketplace API that enables:
- **Farmers** to list and manage their produce
- **Buyers** to browse and purchase agricultural products
- Secure authentication with JWT tokens
- Real-time inventory management

---

## ✨ Features

### User Management
- User registration (Farmers & Buyers)
- JWT-based authentication
- Role-based access control
- Profile management

### Product Management
- Create, read, update, delete products (Farmers only)
- Product categorization (vegetables, fruits, grains, livestock, dairy)
- Inventory tracking
- Search and filtering
- Pagination support

### Security
- Password hashing (bcrypt)
- JWT token authentication
- Role-based authorization
- Protected routes

---

## 🛠 Tech Stack

- **FastAPI** - Web framework
- **SQLAlchemy** - ORM for database operations
- **MySQL 8.0** - Relational database
- **Pydantic** - Data validation
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Uvicorn** - ASGI server
- **JWT (python-jose)** - Authentication tokens
- **bcrypt** - Password hashing

---

## 📁 Project Structure

```
payit/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # Database connection and session
│   ├── enums.py                # Enum definitions
│   │
│   ├── auth/                   # Authentication utilities
│   │   ├── __init__.py
│   │   └── jwt.py              # JWT token creation and verification
│   │
│   ├── models/                 # SQLAlchemy database models
│   │   ├── __init__.py
│   │   ├── base.py             # Base model class
│   │   ├── user.py             # User model
│   │   └── product.py          # Product model
│   │
│   ├── schemas/                # Pydantic schemas (validation)
│   │   ├── __init__.py
│   │   ├── auth.py             # Login schemas
│   │   ├── user.py             # User schemas
│   │   └── product.py          # Product schemas
│   │
│   ├── routes/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py             # Authentication routes
│   │   ├── user.py             # User routes
│   │   └── product.py          # Product routes
│   │
│   └── middlewares/            # Custom middlewares
│       ├── __init__.py
│       └── auth.py             # JWT authentication middleware
│
├── .env                        # Environment variables (not in git)
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore file
├── docker-compose.yml          # Docker compose configuration
├── Dockerfile                  # Docker image definition
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/payit.git
   cd payit
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` file with your credentials**
   ```env
   DB_HOST=payit_db
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=YourSecurePassword123
   DB_DATABASE=payit_db
   FORWARD_DB_PORT=3307

   JWT_SECRET_KEY=your-secret-key-here
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_TIME=60
   ```

4. **Start the application**
   ```bash
   docker-compose up -d --build
   ```

5. **Check if containers are running**
   ```bash
   docker-compose ps
   ```

6. **View logs**
   ```bash
   docker-compose logs -f
   ```

7. **Access the API**
   - API Base URL: `http://localhost:8000`
   - Interactive Docs: `http://localhost:8000/docs`
   - Alternative Docs: `http://localhost:8000/redoc`

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Authentication Endpoints

#### Register User
```http
POST /users/
Content-Type: application/json

{
  "name": "John Farmer",
  "phone": "08012345678",
  "email": "farmer@example.com",
  "password": "Password123!",
  "confirm_password": "Password123!",
  "gender": "male",
  "category": "farmer",
  "location": "Lagos, Nigeria"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "farmer@example.com",
  "password": "Password123!"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "email": "farmer@example.com",
  "user_id": 1
}
```

#### Get Current User
```http
GET /users/me
Authorization: Bearer <your_token>
```

### Product Endpoints

#### Get All Products (Public)
```http
GET /products/?skip=0&limit=10&category=vegetables&search=tomato
```

Query Parameters:
- `skip` - Number of records to skip (default: 0)
- `limit` - Number of records to return (default: 10, max: 100)
- `category` - Filter by category (vegetables, fruits, grains, livestock, dairy, other)
- `status` - Filter by status (available, sold_out, discontinued)
- `search` - Search in product name or location

#### Get Single Product (Public)
```http
GET /products/{product_id}
```

#### Create Product (Farmers Only)
```http
POST /products/
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "name": "Fresh Tomatoes",
  "description": "Organic tomatoes from my farm",
  "category": "vegetables",
  "price_per_unit": 500.50,
  "unit": "kg",
  "quantity_available": 100,
  "location": "Lagos, Nigeria",
  "image_url": "https://example.com/tomatoes.jpg"
}
```

#### Get My Products (Farmers Only)
```http
GET /products/my-products
Authorization: Bearer <your_token>
```

#### Update Product (Owner Only)
```http
PUT /products/{product_id}
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "price_per_unit": 600.00,
  "quantity_available": 80,
  "status": "available"
}
```

#### Delete Product (Owner Only)
```http
DELETE /products/{product_id}
Authorization: Bearer <your_token>
```

---

## 🗄 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    gender ENUM('M', 'F') NOT NULL,
    category ENUM('buyer', 'farmer') NOT NULL,
    location VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email)
);
```

### Products Table
```sql
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    farmer_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category ENUM('vegetables', 'fruits', 'grains', 'livestock', 'dairy', 'other') NOT NULL,
    price_per_unit DECIMAL(10,2) NOT NULL,
    unit ENUM('kg', 'bag', 'piece', 'liter', 'ton', 'crate') NOT NULL,
    quantity_available INT NOT NULL DEFAULT 0,
    image_url VARCHAR(255),
    location VARCHAR(255) NOT NULL,
    status ENUM('available', 'sold_out', 'discontinued') NOT NULL DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_farmer_id (farmer_id)
);
```

### Relationships
- One User (Farmer) can have many Products
- Each Product belongs to one User (Farmer)
- Cascade delete: If a farmer is deleted, their products are also deleted

---

## 🔐 Authentication

### JWT Token Flow

1. **User registers** → Password is hashed with bcrypt
2. **User logs in** → Receives JWT token
3. **User makes request** → Includes token in Authorization header
4. **Server validates token** → Extracts user info and allows access

### Token Structure
```json
{
  "sub": "1",
  "email": "farmer@example.com",
  "user_id": "1",
  "exp": 1234567890
}
```

### Using Tokens in Requests
```bash
curl -X GET http://localhost:8000/products/my-products \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## 💻 Development

### Running Locally (Without Docker)

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up MySQL database**
   ```bash
   mysql -u root -p
   CREATE DATABASE payit_db;
   ```

3. **Update .env for local MySQL**
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your_password
   DB_DATABASE=payit_db
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Database Commands

**Access MySQL in Docker**
```bash
docker exec -it payit_db mysql -u root -p
```

**Run SQL commands**
```sql
USE payit_db;
SHOW TABLES;
DESCRIBE users;
DESCRIBE products;
SELECT * FROM users;
SELECT * FROM products;
```

**Reset Database**
```bash
docker-compose down -v  # Removes volumes (deletes data)
docker-compose up -d --build
```

### Docker Commands

**Start services**
```bash
docker-compose up -d
```

**Stop services**
```bash
docker-compose down
```

**View logs**
```bash
docker-compose logs -f
docker-compose logs -f payit.api
docker-compose logs -f payit_db
```

**Rebuild containers**
```bash
docker-compose up -d --build
```

**Access container shell**
```bash
docker exec -it payit.api /bin/bash
docker exec -it payit_db /bin/bash
```

**Check container status**
```bash
docker-compose ps
docker stats
```

---

## 🧪 Testing

### Manual Testing with cURL

**1. Register a farmer**
```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Farmer",
    "phone": "08012345678",
    "email": "farmer@example.com",
    "password": "Password123!",
    "confirm_password": "Password123!",
    "gender": "male",
    "category": "farmer",
    "location": "Lagos"
  }'
```

**2. Login**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "farmer@example.com",
    "password": "Password123!"
  }'
```

**3. Create a product**
```bash
curl -X POST http://localhost:8000/products/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "name": "Fresh Tomatoes",
    "description": "Organic tomatoes",
    "category": "vegetables",
    "price_per_unit": 500,
    "unit": "kg",
    "quantity_available": 100,
    "location": "Lagos"
  }'
```

**4. Get all products**
```bash
curl http://localhost:8000/products/
```

### Using Postman or Thunder Client

1. Import the API endpoints from `http://localhost:8000/docs`
2. Create an environment with `base_url` = `http://localhost:8000`
3. Test each endpoint

---

## 🔧 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Error: port 8000 is already allocated
# Solution: Change port in docker-compose.yml or stop conflicting service
docker-compose down
sudo lsof -i :8000
kill -9 <PID>
```

#### Database Connection Error
```bash
# Check if database container is running
docker-compose ps

# Check database logs
docker-compose logs payit_db

# Verify .env file has correct credentials
cat .env
```

#### Products Table Not Created
```bash
# Make sure Product model is imported in main.py
# Then rebuild
docker-compose down -v
docker-compose up -d --build
```

#### "Only farmers can create products"
```bash
# Make sure you registered with category: "farmer"
# Check your user in database
docker exec -it payit_db mysql -u root -p
USE payit_db;
SELECT id, email, category FROM users;
```

#### Module Import Errors
```bash
# Rebuild the container
docker-compose up -d --build

# Check for syntax errors
docker-compose logs payit.api
```

---

## 📝 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DB_HOST` | Database hostname | `payit_db` |
| `DB_PORT` | Database port | `3306` |
| `DB_USER` | Database username | `root` |
| `DB_PASSWORD` | Database password | `YourPassword123` |
| `DB_DATABASE` | Database name | `payit_db` |
| `FORWARD_DB_PORT` | Host port for database | `3307` |
| `JWT_SECRET_KEY` | Secret key for JWT tokens | `your-secret-key` |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `JWT_EXPIRATION_TIME` | Token expiry in minutes | `60` |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👥 Authors

- **Your Name** - Initial work

---

## 🙏 Acknowledgments

- FastAPI documentation
- SQLAlchemy documentation
- Docker documentation

---

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Email: support@payit.com

---

## 🗺 Roadmap

- [ ] Order management system
- [ ] Payment integration
- [ ] Review and rating system
- [ ] Image upload functionality
- [ ] Email notifications
- [ ] SMS notifications
- [ ] Admin dashboard
- [ ] Analytics and reporting

---

**Built with ❤️ for farmers and buyers**
