FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --force-reinstall -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose port
EXPOSE 5000

# Start with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
