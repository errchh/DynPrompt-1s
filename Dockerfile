# Specify platform for compatibility
FROM --platform=linux/amd64 ollama/ollama:latest

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 11434
EXPOSE 8501

# Create shell script
RUN echo '#!/bin/bash \n\
ollama serve & \n\
sleep 5 \n\
ollama pull llama3.2:3b \n\
exec streamlit run ui.py --server.port=8501 --server.address=0.0.0.0 llama3.2:3b \n\
' > /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
