FROM python:3.11-slim

WORKDIR /app

# Copy requirements and package files
COPY requirements.txt .
COPY pyproject.toml .
COPY src/ ./src/

# Install dependencies including the package itself
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Streamlit port
EXPOSE 8501

# Headless configuration for Streamlit
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

CMD ["streamlit", "run", "app.py"]
