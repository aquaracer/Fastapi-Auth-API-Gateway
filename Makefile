.DEFAULT_GOAL := help

run: ## Run the application using uvicorn with provided arguments and defaults
	#poetry run gunicorn src.main:src --worker-class uvicorn.workers.UvicornWorker -c gunicorn.conf.py
	poetry run uvicorn src.main:app

install: ## Install a dependency using poetry
	@echo "Installing dependency $(LIBRARY)"
	poetry add $(LIBRARY)

uninstall: ## Uninstall a dependency using poetry
	@echo "Uninstalling dependency $(LIBRARY)"
	poetry remove $(LIBRARY)

migrate-create:
	alembic revision --autogenerate -m $(MIGRATION)

migrate-apply:
	alembic upgrade head

help: ## Show this help message
	@echo "Usage make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf " %-20s %s\n", $$1, $$2}'


