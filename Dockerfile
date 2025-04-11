FROM downloads.unstructured.io/unstructured-io/unstructured:latest

# Set environment variable to ensure Python output is sent straight to terminal
ENV PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 libgl1 -y  \
    && apt-get clean

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Define the default command to run your app
CMD ["python", "src/run.py"]
