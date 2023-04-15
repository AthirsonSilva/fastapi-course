FROM python:3.11

WORKDIR /app

COPY requirements.txt ./

EXPOSE 8000

# Activate virtualenv
RUN virtualenv venv
RUN . venv/bin/activate

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
RUN pip install psycopg2

# Run the application
RUN uvicorn src.main:app --host