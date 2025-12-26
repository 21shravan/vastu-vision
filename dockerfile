FROM python:3.11-slim

# Install system dependencies required by WeasyPrint
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libcairo2 \
    libglib2.0-0 \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy project files
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Streamlit runs on 8501
EXPOSE 8501

# Start Streamlit app
CMD ["streamlit", "run", "streamlit_invoice_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
