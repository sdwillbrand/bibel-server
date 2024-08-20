FROM python:3.11.2
WORKDIR /app
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./src .
CMD ["uvicorn", "main:app", "--port", "3333"]