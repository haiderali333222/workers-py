FROM python:3.10.4

WORKDIR /src

RUN apt-get update -y && apt-get install -y --no-install-recommends \
  curl \
  gcc \
  g++ \
  gnupg \
  unixodbc-dev && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

# Install virtualenv
RUN pip install virtualenv

# Set up the virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies in the virtual environment
RUN pip install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose the server ports
EXPOSE 8888

# Specify the default command to run the application
CMD ["python", "main.py"]
