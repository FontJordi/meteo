FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the Python script into the container
COPY producer.py .

# Install the required Python packages
RUN pip install kafka-python

# Command to run the Python script, wait for the kafka brokers to be initialized
CMD ["sh", "-c", "sleep 30 && python producer.py"] 
