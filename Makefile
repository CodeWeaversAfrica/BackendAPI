# Define variables
COMPOSE_FILE = docker-compose.yaml
WEB_SERVICE = web

.PHONY: build up down logs shell migrate makemigrations build-up test createsuperuser startapp collectstatic

# Build Docker images
build:
	docker-compose -f $(COMPOSE_FILE) build

# Start the services in detached mode
up:
	docker-compose -f $(COMPOSE_FILE) up -d

# Build and start the services in detached mode
build-up:
	docker-compose -f $(COMPOSE_FILE) up -d --build

# Stop and remove containers, networks, images, and volumes
down:
	docker-compose -f $(COMPOSE_FILE) down

# View logs of the services
logs:
	docker-compose -f $(COMPOSE_FILE) logs

# Open a shell in the web service container
shell:
	docker-compose -f $(COMPOSE_FILE) exec $(WEB_SERVICE) /bin/bash

# Run Django migrations
migrate:
	docker-compose -f $(COMPOSE_FILE) exec $(WEB_SERVICE) python manage.py migrate

# Create new Django migrations
makemigrations:
	docker-compose -f $(COMPOSE_FILE) exec $(WEB_SERVICE) python manage.py makemigrations

# Run tests (if you have a test command)
test:
	docker-compose -f $(COMPOSE_FILE) exec $(WEB_SERVICE) python manage.py test

# Create a new Django app (usage: make startapp APP_NAME=your_app_name)
startapp:
	docker-compose -f $(COMPOSE_FILE) exec $(WEB_SERVICE) python manage.py startapp $(APP_NAME)

# Create a superuser (usage: make createsuperuser)
createsuperuser:
	docker-compose -f $(COMPOSE_FILE) exec $(WEB_SERVICE) python manage.py createsuperuser

# Collect static files (usage: make collectstatic)
collectstatic:
	docker-compose -f $(COMPOSE_FILE) exec $(WEB_SERVICE) python manage.py collectstatic --noinput
