FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md /app/
COPY rooomtech_dap /app/rooomtech_dap
RUN pip install --no-cache-dir .

EXPOSE 8080
CMD ["uvicorn", "rooomtech_dap.api:app", "--host", "0.0.0.0", "--port", "8080"]
