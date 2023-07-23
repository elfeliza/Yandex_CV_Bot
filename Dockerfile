FROM python:3.10.7-alpine3.16

RUN pip install --upgrade pip

WORKDIR /usr/src/app/
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "main.py"]