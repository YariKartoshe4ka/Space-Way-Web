FROM python:3.9

# Install Dart SASS
RUN curl -L https://github.com/sass/dart-sass/releases/download/1.51.0/dart-sass-1.51.0-linux-x64.tar.gz -o /tmp/sass.tar.gz && \
    tar -xzf /tmp/sass.tar.gz -C /tmp && \
    mv /tmp/dart-sass/sass /bin/sass

# Add new user for app
RUN useradd -ms /bin/bash app

# Switch to created user and configure it
USER app
RUN mkdir /home/app/web
WORKDIR /home/app/web
ENV PATH="${PATH}:/home/app/.local/bin"

# Setup environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Python requirements
COPY --chown=app:app app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy app files
COPY --chown=app:app app .

# Generate CSS files
RUN mkdir web/static/css
RUN sass -s compressed web/static/scss/index.scss web/static/css/index.css

# Expose web port
EXPOSE 8000

# Copy entrypoint script
COPY docker-entrypoint.sh /

CMD ["/docker-entrypoint.sh"]
