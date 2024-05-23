# FastApi-Celery-Redis

Example of implementations a simple FastApi app with Celery tasks 

## Endpoints

- `/`: Hello world endpoint
- `/upload_files`: Upload files endpoint

## Celery tasks

1. `task that handles the upload of files`
2. `task that starts periodically and sends a message to the broker every 10 seconds`


## Project structure
- `controllers/*`: Contains the FastApi logic for each endpoint
- `views/*`: Contains the FastApi endpoints
- `data/*`: Contains the test data files
- `celery_worker.py`: Contains the Celery tasks
- `main.py`: Contains the FastApi app entrypoint
- `requirements.txt`: Contains the Python dependencies

## How to run the project

1. Clone the repository
2. Install all libraries using pip install -r requirements.txt
3. python ./main.py
4. Open http://0.0.0.0:8888/docs in your browser to see the Swagger UI
5. Open http://0.0.0.0:5556/ in your browser to see the Flower UI
