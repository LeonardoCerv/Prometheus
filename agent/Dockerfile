# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8080 for Cloud Run (Cloud Run expects PORT env var)
EXPOSE 8080

# Set default environment variables (can be overridden at runtime)
ENV PORT=8080
ENV GOOGLE_GENAI_USE_VERTEXAI=FALSE

# Use the ADK CLI to run the web server as documented
# Format: adk web --agent <module>:<agent_variable>
CMD adk web --agent agent:root_agent --port ${PORT} --host 0.0.0.0
