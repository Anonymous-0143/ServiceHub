# 🛠️ ServiceHub

A full-stack **Django** web application that connects customers with trusted local service providers. Built with a modern **claymorphism UI** and role-based authentication.

---

## ✨ Features

### For Customers
- Browse service categories (Plumbing, Electrical, Cleaning, etc.)
- View available providers per category
- Book service providers with date, time, and address
- Track bookings from a personal dashboard
- Cancel pending bookings
- Edit profile (name, email, phone)

### For Service Providers
- Register with service category, experience, location, and hourly rate
- View incoming booking requests on a dedicated dashboard
- Accept or reject bookings
- Edit profile and service details

### General
- **Role-based registration** — choose Customer or Provider at signup
- **Claymorphism UI** — modern, puffy card design with layered shadows
- **Personalized greetings** — "Hello, [Name]" on home and dashboard
- **Profile icon** — round avatar in the top-right corner linking to profile page
- **Email notifications** via SMTP
- **Responsive sidebar** navigation

---

## 🛠️ Tech Stack

| Layer      | Technology          |
|------------|---------------------|
| Backend    | Django 5.2, Python 3.11 |
| Frontend   | HTML, CSS, Bootstrap 5.3 |
| Database   | SQLite              |
| Font       | Inter (Google Fonts) |
| Design     | Claymorphism         |

---

## 📁 Project Structure

```
LocalService/
├── servicehub/              # Django project root
│   ├── accounts/            # Custom User model, registration, profile
│   ├── services/            # Categories, ProviderProfile, views
│   ├── bookings/            # Booking model
│   ├── templates/           # All HTML templates
│   │   ├── base.html        # Layout with sidebar + profile icon
│   │   ├── home.html        # Landing page / service listing
│   │   ├── dashboard.html   # Customer bookings dashboard
│   │   ├── providers.html   # Provider cards with claymorphism
│   │   ├── profile.html     # Profile edit page
│   │   ├── provider_dashboard.html
│   │   ├── book_provider.html
│   │   └── registration/    # Login, register, role selection
│   └── servicehub/          # Settings, URLs, WSGI
├── env/                     # Virtual environment (not tracked)
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Anonymous-0143/ServiceHub.git
cd ServiceHub

# Create and activate virtual environment
python -m venv env
env\Scripts\activate        # Windows
# source env/bin/activate   # macOS/Linux

# Install dependencies
pip install django

# Run migrations
cd servicehub
python manage.py migrate

# Create a superuser (for admin panel)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

### Access the App
- **App**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## 📸 Pages Overview

| Page | URL | Description |
|------|-----|-------------|
| Home (Landing) | `/` | Hero section for guests, service listing for customers |
| Register | `/accounts/register/` | Choose role → fill form |
| Login | `/accounts/login/` | Sign in |
| Profile | `/accounts/profile/` | Edit personal & service details |
| Providers | `/providers/<category_id>/` | Browse providers in a category |
| Book Provider | `/book/<provider_id>/` | Booking form |
| Dashboard | `/dashboard/` | Customer's bookings |
| Provider Dashboard | `/provider/dashboard/` | Manage incoming bookings |

---

## 👤 User Roles

| Role | Can Do |
|------|--------|
| **Customer** | Browse services, book providers, track bookings, edit profile |
| **Provider** | Receive bookings, accept/reject, edit service details |
| **Admin** | Full access via Django admin panel |

---

## 📄 License

This project is for educational purposes.

---
