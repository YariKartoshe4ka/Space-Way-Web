SHELL:=/bin/bash

setup: setup-env setup-venv setup-scss
clean: clean-venv clean-scss


setup-env: # Prepare file with environment variables
	cp -n app/.env.example app/.env


setup-venv: # Build virtual environment of project
	python3 -m pip install virtualenv
	virtualenv venv
	. venv/bin/activate && pip install -r app/requirements.txt

clean-venv: # Remove virtual environment
	rm -rf venv


setup-scss: # Parse SCSS to compressed CSS files
	mkdir -p app/web/static/css
	sassc -t compressed app/web/static/scss/index.scss app/web/static/css/index.css

clean-scss: # Remove all CSS files
	find app -depth -name "*.css" -type f -exec rm -f {} \;


db: # Setup database
	sudo -u postgres -- $(SHELL) -c ' \
		. app/.env && \
		psql -c "CREATE USER $$POSTGRES_USER WITH PASSWORD '\'$$POSTGRES_PASSWORD\'';" && \
		createdb -O $$POSTGRES_USER $$POSTGRES_DB; \
	' || true

	. venv/bin/activate; \
	cd app; \
	python manage.py makemigrations; \
	python manage.py migrate; \
	python manage.py createsuperuser --no-input || true


deps: # Install all dependencies via APT
	sudo apt-get update
	sudo apt-get install -y \
		python3 \
		python3-pip \
		docker.io \
		docker-compose \
		postgresql \
		sassc
