# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /src

# Copy the current directory contents into the container at /app
COPY . /src 

# Install any needed packages specified in requirements.txt
RUN pip install -r ../requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
