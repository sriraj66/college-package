FROM python:3.11


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]