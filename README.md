# AI-Dev-Tools

## Setup Instructions

### 1. Install Python, pip, and venv

Ensure you have Python, pip, and venv installed on your system.
```bash
sudo apt update && sudo apt install -y python3 python3-pip python3-venv
```

### 2. Install uv
uv is a fast Python package installer and resolver. Install it using the following command:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Create and Activate Virtual Environment
It's recommended to work within a virtual environment.

```bash
uv venv
source .venv/bin/activate
```

### 4. Install Django
With your virtual environment active, install Django using uv:

```bash
uv pip install django
```

### 5. Run Database Migrations
After setting up your models, apply the database migrations:

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

### 6. Run the Django Application
Start the development server:

```bash
uv run python manage.py runserver
```

Then, open the application in your browser:

```bash
"$BROWSER" http://127.0.0.1:8000/
```

### 7. Testing

```bash
python manage.py test
```

## Tree project
```bash
├── README.md
├── db.sqlite3
├── manage.py
├── todo_app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── templates
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── todo_project
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```