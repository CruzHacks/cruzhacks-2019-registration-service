FROM python:3.6.5-alpine3.7
RUN apk update
RUN apk add sudo --no-cache
COPY requirements.txt backend/requirements.txt
RUN pip install -r backend/requirements.txt
COPY . backend
EXPOSE 5000
CMD ["python", "-u", "./src/api.py"]
