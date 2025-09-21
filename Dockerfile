FROM node:18-alpine

# Install Python for the content pipeline
RUN apk add --no-cache python3 py3-pip

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy application code
COPY . .

# Create data directory for SQLite database
RUN mkdir -p data

# Expose Ghost port
EXPOSE 2368

# Start Ghost and the content pipeline
CMD ["sh", "-c", "docker-compose up ghost"]