FROM python:3.9-slim-bullseye

WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt
COPY recommendation_ui.py .

EXPOSE 8502
ENTRYPOINT ["streamlit", "run", "recommendation_ui.py", "--server.port=8502", "--server.address=0.0.0.0"]
