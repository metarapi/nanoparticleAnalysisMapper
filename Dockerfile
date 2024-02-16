# Use a Python base image
FROM python:3.10.6-slim-buster

# Set environment variables
ENV PYTHONPATH=/app:$PYTHONPATH
ENV DJANGO_SETTINGS_MODULE=mysite.settings
ENV SECRET_KEY=django-insecure-4eb0yr(!v$t2$gqg7@)%_t^ytud!8=2a#f5e&s8@_f_afh$7o^
ENV DEBUG=True

# Copy project files into the Docker image
COPY . /app

# Install project dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Set the working directory
WORKDIR /app

# Install Daphne
RUN pip install daphne

# Expose the application port
EXPOSE 8000

# Run the application with Daphne
CMD ["daphne", "-u", "/tmp/daphne.sock", "-b", "0.0.0.0", "-p", "8000", "mysite.asgi:application"]