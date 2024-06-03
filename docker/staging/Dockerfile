FROM python:3.10-slim-buster

WORKDIR /src

RUN apt-get update -y && apt-get install -y --no-install-recommends \
  curl \
  gcc \
  g++ \
  gnupg \
  unixodbc-dev && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip3 install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Add the environment variables file
ADD .env .

# Expose the server ports
EXPOSE 8888

# Specify the default command to run the application
CMD ["python3", "main.py"]
