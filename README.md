# Competitor URL Scraping API Documentation

## Project Overview

This project is a FastAPI-based web service designed to scrape competitor URLs. It utilizes Celery for task management and Redis as the message broker. The API enqueues URL fetch tasks for specified competitors and monitors the status of these tasks. Additionally, the system integrates with Slack for notification purposes.

## Requirements

Below is a list of the main dependencies and their versions required to run this project:

- Python 3.8+
- Redis server
- Slack Webhook URL for notifications
- MongoDB

## How to Run

### Prerequisites

- Python 3.8+
- Redis server
- Slack Webhook URL for notifications
- MongoDB

### Setup

1. **Clone the Repository**

   ```sh
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Install Dependencies**

   ```sh
   pip install -r requirements.txt
   ```

3. **Start Redis Server**

   ```sh
    redis-server --daemonize yes
   ```

4. **Start MongoDB Server**

   ```sh
    sudo systemctl start mongod
   ```

5. **Set Environment Variables**

   Create a `.env` file in the root directory by copying the contents of the `.env.example` file and updating the values as needed.

   ```sh
    CELERY_BROKER_URL=redis://localhost:6379/0
    CELERY_RESULT_BACKEND=redis://localhost:6379/0
    ENVIRONMENT=local
    DB_URL=mongodb://127.0.0.1:27017/
    DB_NAME=pricing
    ELASTIC_SEARCH_URL=
    ELASTIC_SEARCH_USERNAME=
    ELASTIC_SEARCH_PASSWORD=
    API_KEY_SCRAPY=
    PROXY_CSV_URL=
    SLACK_HEADER=
    REDIS_URL=redis://localhost:6379/0
   ```

6. **Run the Application**

   ```sh
    python3 main.py
   ```

7. **Access the API**

   The API will be accessible at `http://localhost:8000`.

## API Documentation

The API documentation can be accessed at `http://localhost:8000/docs`.

### Endpoints

#### 1. Enqueue URL Fetch Task

- **URL**: `/enqueue`
- **Method**: `POST`
- **Request Body**:

  ```json
  {
    "competitors": ["competitor1", "competitor2"]
  }
  ```

- **Response**:

  ```json
  {
    "task_ids": {
      "competitor1": "task_id_1",
      "competitor2": "task_id_2"
    },
    "message": "URL Fetch tasks for [competitor1, competitor2] have been enqueued",
    "non_existent_competitors": []
  }
  ```

#### 2. Get Task Status

- **URL**: `/status/{task_id}`
- **Method**: `GET`
- **Response**:

  ```json
  {
    "task_id": "task_id_1",
    "status": "SUCCESS",
    "result": "Task result data"
  }
  ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
### Output[]: # Path: README.md
```
