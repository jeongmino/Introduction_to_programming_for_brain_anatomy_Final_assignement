# ----------------------------------------
# Base image
# ----------------------------------------
FROM python:3.11-slim

# ----------------------------------------
# Set working directory
# ----------------------------------------
WORKDIR /app

# ----------------------------------------
# Install system dependencies (for scipy, matplotlib)
# ----------------------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------------------
# Copy dependency list and install
# ----------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------------------
# Copy project source code
# ----------------------------------------
COPY analysis/ analysis/
COPY main.py .
COPY mouseLFP.mat .

# ----------------------------------------
# Default command
# ----------------------------------------
CMD ["python", "main.py"]
