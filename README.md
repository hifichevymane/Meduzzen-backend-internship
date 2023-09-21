# Meduzzen-backend-intership

Meduzzen backend intership

## How to start the project using Docker

1. Go to the `/meduzzen_backend` folder:

```sh
cd /meduzzen_backend
```

2. Create `.env` file in `/meduzzen_backend` directory and paste all needed variables like in `.env.sample` file

3. Build and run the Docker compose file:

```sh
docker-compose up --build
```

4. Go to the `localhost:8000` in your browser:

## How to run tests within a Docker container

1. Run docker-compose file with detached mode:

```sh
docker-compose up -d
```

2. Run this command in terminal:

```sh
docker-compose run web python manage.py test
```

## How to start the project not using Docker

1. Create an virtual enviroment:

```sh
python -m venv venv
```

2. Activate the virtual environment:
   > Windows

```sh
venv\Scripts\activate
```

> Linux/ MacOS

```sh
source venv/bin/activate
```

3. Go to the `/meduzzen_backend` directory:

```sh
cd /meduzzen_backend
```

4. Install all dependencies from `requirements.txt`:

```sh
pip install -r requirements.txt
```

5. Create `.env` file in `/meduzzen_backend` directory and paste all needed variables like in `.env.sample` file

6. Run this command:

```sh
python manage.py runserver
```

7. Go to http://127.0.0.1:8000/ in your browser

## How to run tests not using Docker

1. Go to `/meduzzen_backend` directory:
   ```sh
   cd /meduzzen_backend
   ```
2. Run this command in a terminal:
   ```sh
   python manage.py test
   ```
