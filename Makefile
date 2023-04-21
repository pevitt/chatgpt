build: ## Build the base image
	docker compose build

up: ## Up container
	docker compose up

makemigrations: ## Run django makemigrations command
	docker compose run web python manage.py makemigrations

migrate: ## Run django migrate command
	docker compose run web python manage.py migrate

shell: ## Run django shell_plus command
	docker compose run web python manage.py shell

test: ## Run django shell_plus command
	docker compose run web pytest

docker-exec: ## Run django shell_plus command make docker-exec CONTAINER_ID=244ff84b4b81 ARGS=pytestmkw
	docker exec -it $(CONTAINER_ID) $(ARGS)
