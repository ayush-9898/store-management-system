# 🏪 Store Management System

A full-featured store management web application built with **Django 6.0.2**, providing tools to manage inventory, customers, staff, and billing — all in one place.

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Database Setup](#database-setup)
  - [Running the Server](#running-the-server)
- [Modules Overview](#modules-overview)
- [Management Commands](#management-commands)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

- 📦 **Inventory Management** — Add, update, and delete products and suppliers; track returnable items
- 👥 **Customer Management** — Maintain a customer directory with contact details
- 🧾 **Billing** — Create and list invoices with ease
- 👨‍💼 **Staff Management** — Manage staff records with role-based access control via decorators
- 📊 **Dashboard** — At-a-glance overview of key store metrics
- 🔔 **Low Stock Alerts** — Built-in management command to detect low-stock products
- 🔗 **REST API** — Django REST Framework integration for API access

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.x, Django 6.0.2 |
| REST API | Django REST Framework 3.16.1 |
| Database | PostgreSQL (psycopg2-binary 2.9.11) |
| Frontend | Bootstrap, HTML/CSS |
| Utilities | sqlparse, tzdata |

---

## 📁 Project Structure

```
store_project/
├── billing/               # Invoice creation and listing
│   ├── models.py          # Invoice model
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/billing/
│       ├── create_invoice.html
│       └── invoice_list.html
│
├── customers/             # Customer management
│   ├── models.py          # Customer model (name, phone)
│   ├── views.py
│   ├── urls.py
│   └── templates/customers/
│       └── customer_list.html
│
├── home/                  # Dashboard & landing
│   ├── views.py           # Aggregates store-wide data
│   └── templates/home/
│       ├── index.html
│       └── dashboard.html
│
├── inventory/             # Product & supplier management
│   ├── models.py          # Product (is_returnable), Supplier
│   ├── views.py
│   ├── urls.py
│   ├── management/commands/
│   │   └── low_stock_alert.py
│   └── templates/inventory/
│
├── staff/                 # Staff management
│   ├── models.py          # Staff (name, phone, joining_date)
│   ├── decorators.py      # Access control decorators
│   ├── views.py
│   ├── urls.py
│   └── templates/staff/
│
└── store_project/         # Project config
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- pip

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/store-management.git
cd store-management
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install django==6.0.2 djangorestframework==3.16.1 psycopg2-binary==2.9.11 sqlparse tzdata
```

### Database Setup

1. Create a PostgreSQL database:

```sql
CREATE DATABASE store_db;
CREATE USER store_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE store_db TO store_user;
```

2. Update `store_project/settings.py` with your database credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'store_db',
        'USER': 'store_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser:

```bash
python manage.py createsuperuser
```

### Running the Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

---

## 📦 Modules Overview

### 🏠 Home
The landing dashboard that aggregates data from all modules — gives a quick summary of inventory, customers, staff, and recent billing activity.

### 📦 Inventory
Manage your product catalog and suppliers. Products support an `is_returnable` flag. Supports full CRUD operations.

### 👥 Customers
Store and manage customer information including name and phone number. Supports full CRUD operations.

### 🧾 Billing
Create invoices and view a complete invoice list. Linked to customer records for accurate billing.

### 👨‍💼 Staff
Manage staff records (name, phone, joining date). Includes custom decorators for access control to restrict sensitive views.

---

## ⚙️ Management Commands

### Low Stock Alert

Detect products that have fallen below the minimum stock threshold:

```bash
python manage.py low_stock_alert
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

