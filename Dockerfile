# Use an official Python runtime as a parent image
FROM ksketo/python-pillow
ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST "redis"
#   ENV POSTGRES_HOST "postgres"
RUN mkdir /citas
# Set the working directory to /citas
WORKDIR /citas

# Copy the current directory contents into the container at /citas
ADD . /citas

# Install any needed packages specified in dependencias.txt
RUN pip install --upgrade pip
RUN pip install -r requerimientos.txt
# RUN python manage.py makemigrations
# RUN python manage.py migrate
# RUN python manage.py loaddata db.json
# Run python when the container launches
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
