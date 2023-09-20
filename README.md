# Meduzzen-backend-intership

Meduzzen backend intership

## How to start the project

1. Create an virtual enviroment:
   `python -m venv venv`
2. Activate the virtual environment:
   > Windows
   > `venv\Scripts\activate`
   > Linux/ MacOS
   > `source venv/bin/activate`
3. Install all dependencies from `requirements.txt`:
   `pip install -r requirements.txt`
4. Create `.env` file in `/meduzzen_backend` directory and paste all needed variables like in `.env.sample` file
5. Go to the `/meduzzen_backend` directory:
   `cd /meduzzen_backend`
6. Run this command:
   `python manage.py runserver`
7. Go to http://127.0.0.1:8000/ in your browser

## How to run tests

1. Go to `/meduzzen_backend` directory:
   `cd /meduzzen_backend`
2. Run this command in a terminal:
   `python manage.py test`
