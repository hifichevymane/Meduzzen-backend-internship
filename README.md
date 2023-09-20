# Meduzzen-backend-intership

Meduzzen backend intership

## How to start the project using Docker

1. Go to the `/meduzzen_backend` folder:
   ```sh
   cd /meduzzen_backend
   ```
2. Create the Docker image:
   ```sh
   docker build --tag meduzzen_backend .
   ```
3. Run the Docker image:
   ```sh
   docker run --env-file ./.env --publish 8000:8000 meduzzen_backend
   ```
4. Go to the `localhost:8000` in your browser:

## How to run tests within a Docker container

1. Make sure you've run a Docker container:
   ```sh
   docker ps
   ```
2. If you see message like this:

   ```
   CONTAINER ID   IMAGE              COMMAND                  CREATED         STATUS         PORTS                    NAMES
   container-id  meduzzen_backend   "python3 manage.py r…"   2 minutes ago   Up 2 minutes   0.0.0.0:8000->8000/tcp   container-name
   ```

   That means that the container is running

3. Run tests within the Docker container:
   ```sh
   docker exec -it container-id/container-name python manage.py test
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
3. Install all dependencies from `requirements.txt`:
   ```sh
   pip install -r requirements.txt
   ```
4. Create `.env` file in `/meduzzen_backend` directory and paste all needed variables like in `.env.sample` file
5. Go to the `/meduzzen_backend` directory:
   ```sh
   cd /meduzzen_backend
   ```
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
