FROM python:3.7-slim
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY . /app
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]
