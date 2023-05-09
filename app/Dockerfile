FROM python:3.8.16-bullseye

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py migrate portfolioviz
RUN python manage.py add_initial_data
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]