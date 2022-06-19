# Backend For Restaurant App Implemented With Django
This is meant to implement the backend for the Restaurant App with Django. You can read the following instructions to set up and work with the backend.

# API
The backend is served on:
```bash
http://127.0.0.1:8000/
```
To access the admin page, navigate to:
```bash
http://127.0.0.1:8000/admin
```
The API of the backend is defined along:
```bash
http://127.0.0.1:8000/api
```
You can look up django/app/app/urls.py and django/app/restaurants/urls.py to find out more about the available API routes.

# Set up
Navigate to django directory
```bash
cd django
```
Create virtual environment
```bash
python -m venv env
```
Activate the virtual environment
```bash
env\Scripts\activate
```
Install packages specified in requirements.txt
```bash
python -m pip install -r requirements.txt
```
IMPORTANT! The below code require navigation to the app directory
```bash
cd app
```

# Start the development server
Run migrations (necessary for first time running the server or after change of models)
```bash
python manage.py migrate
```
Start the server
```bash
python manage.py runserver
```

# After change of models
Make migrations
```bash
python manage.py makemigrations
```
Run migrations
```bash
python manage.py migrate
```

# Others
Create super user
```bash
python manage.py createsuperuser
```
