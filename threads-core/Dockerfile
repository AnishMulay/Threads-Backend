FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Add the current directory to /opt
ADD . /opt
WORKDIR /opt

# Update package lists and install necessary packages
RUN apt-get update && apt-get install -y dos2unix

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Ensure the deploy.sh script has Unix line endings and is executable
RUN dos2unix /opt/deploy.sh && chmod +x /opt/deploy.sh

# Expose port 5000 (assuming your Flask app runs on this port)
EXPOSE 5000

# Set the entrypoint to run the deploy.sh script
ENTRYPOINT ["./deploy.sh"]