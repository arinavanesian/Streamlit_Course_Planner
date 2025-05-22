FROM python:3.9-slim-bookworm as builder

WORKDIR /app
COPY requirements.txt .

RUN pip install --user -r requirements.txt

FROM python:3.9-slim-bookworm

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app


EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
