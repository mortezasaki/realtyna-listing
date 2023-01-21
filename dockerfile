# Pull official base Python Docker image
FROM python:3.10.6
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=realtyna.settings.prod
# Set work directory
WORKDIR /realtyna
# Install dependencies
RUN pip install --upgrade pip

COPY requirements /realtyna/requirements
RUN pip install -r /realtyna/requirements/prod.txt
# Copy the Django project
COPY ./src/project /realtyna

RUN python manage.py migrate