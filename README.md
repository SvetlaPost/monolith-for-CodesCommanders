# Monolith for CodesCommanders

This API was built as a test assignment for a backend internship at CodesCommanders.
It’s a monolithic Django application with user management (registration, login, profile) and basic order handling.
The app uses PostgreSQL and runs in a fully Dockerized environment.

##  Features

-  Custom user model with roles: **Admin**, **User**, **Moderator**
-  JWT-based authentication (`djangorestframework-simplejwt`)
-  Registration, login, logout, token refresh
-  Profile update and user list (admin)
-  Order creation, listing, updating, deleting (owner only)
-  Permissions for safe access (e.g., user can only modify own orders)
-  Pagination-ready setup
-  Admin panel support
-  Dockerized environment with PostgreSQL

---

## Project Structure

monolith-for-CodesCommanders/
│
├── applications/
│ ├── users/ # User app (models, views, serializers, permissions)
│ └── orders/ # Order app (models, views, permissions)
│
├── proj/ # Django core project (settings, URLs, wsgi)
│
├── Dockerfile # App Docker image
├── docker-compose.yml # Full setup (PostgreSQL + Django)
├── .env # Environment variables (excluded in .gitignore)
├── requirements.txt
└── README.md


---

## Installation & Usage

### Prerequisites

- Python 3.10+
- Docker and Docker Compose

---

### 1. Clone the repository

```bash
git clone https://github.com/SvetlaPost/monolith-for-CodesCommanders.git
cd monolith-for-CodesCommanders

---

### 2. Set up .env
Create a .env file in the root directory:

SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

POSTGRES_DB=monolith_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

---

### 3. Run via Docker

docker compose up --build

---

### 4. Apply migrations and create superuser

docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser

---

### 5. API Endpoints

| Method | Endpoint               | Description             |
| ------ | ---------------------- | ----------------------- |
| POST   | `/api/users/register/` | Register a new user     |
| POST   | `/api/users/login/`    | Log in with credentials |
| GET    | `/api/users/`          | List all users (admin)  |
| POST   | `/api/orders/`         | Create a new order      |
| GET    | `/api/orders/`         | List all orders         |

---
### 6. Admin Access

Visit http://localhost:8000/admin/
Login with your superuser credentials.

---
### 7.Author

Svetlana Postel
Test task for CodesCommanders internship program.





