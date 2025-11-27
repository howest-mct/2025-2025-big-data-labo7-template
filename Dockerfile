FROM python:3.14.0-alpine3.22

RUN addgroup -S app && adduser -S app -G app

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY youtube.py ./

RUN chown -R app:app /app

USER app

CMD ["python", "youtube.py"]
