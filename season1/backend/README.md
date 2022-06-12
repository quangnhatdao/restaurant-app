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
venv\Scripts\activate
```
### Install packages specified in requirements.txt
```bash
python -m pip install -r requirements.txt
```

## 2. Start the development server

### Navigate to app directory
```bash
cd app
```
### Start the server
```bash
python manage.py runserver
```

## 3. After change the models

### Navigate to app directory
```bash
cd app
```
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