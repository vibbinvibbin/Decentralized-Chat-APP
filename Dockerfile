FROM python:3.12 AS base
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

FROM base 

COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
