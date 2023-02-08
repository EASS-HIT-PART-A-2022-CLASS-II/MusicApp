FROM python:3.9
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY . .

EXPOSE 80

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
# ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=80", "--server.address=0.0.0.0"]