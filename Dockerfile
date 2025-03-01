# Base image configuration
# Using linux/amd64 platform for compatibility with Mac M1/M2 chips
FROM --platform=linux/amd64 ollama/ollama:latest

# System dependencies
# Update package list and install Python with pip
# Clean up apt cache to reduce image size
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Dependencies installation
# Copy requirements file first to leverage Docker cache
COPY requirements.txt .
# Install Python packages specified in requirements.txt
# --no-cache-dir reduces image size
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application files
# Copy all files from current directory to container
COPY . .

# Port configuration
# Expose port for Ollama API service
EXPOSE 11434
# Expose port for Streamlit web interface
EXPOSE 8501

# Startup script creation
# Create shell script to:
# 1. Start Ollama service
# 2. Wait for service initialization
# 3. Pull specified LLM model
# 4. Launch Streamlit application
RUN echo '#!/bin/bash \n\
ollama serve & \n\
sleep 5 \n\
ollama pull llama3.2:3b \n\
exec streamlit run ui.py --server.port=8501 --server.address=0.0.0.0 llama3.2:3b \n\
' > /app/entrypoint.sh

# Set execute permissions for startup script
RUN chmod +x /app/entrypoint.sh

# Container startup command
# Execute the startup script using bash
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
