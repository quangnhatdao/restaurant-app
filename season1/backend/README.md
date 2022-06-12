# Backend Server For Restaurant App Implemented With Django

## 1. Set up

### Navigate to django directory
```bash
cd django
```

### Create virtual environment
```bash
python -m venv env
```
### Activate the virtual environment
```bash
env\Scripts\activate
```
### Install packages specified in requirements.txt
```bash
python -m pip install -r requirements.txt
```

## IMPORTANT: The below code require navigation to the app directory
```bash
cd app
```

## 2. Start the development server

### Run migrations (If you have not already)
```bash
python manage.py migrate
```
### Start the server
```bash
python manage.py runserver
```

## 3. After change the models

### Make migrations
```bash
python manage.py makemigrations
```
### Run migrations
```bash
python manage.py migrate
```

## 4. Others

### Create super user
```bash
python manage.py createsuperuser
```