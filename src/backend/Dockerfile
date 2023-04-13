FROM python:3.9

WORKDIR /dist

COPY ./ /dist

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]