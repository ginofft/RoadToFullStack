FROM python:3.9-slim

WORKDIR /dist

COPY ./requirements.txt /dist/requirements.txt

RUN pip install --no-cache-dir -r /dist/requirements.txt 
COPY . /dist

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]