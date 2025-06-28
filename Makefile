MIGRATIONS_DIR = db/migrations
TIMESTAMP = $(shell date +%Y%m%d%H%M%S)
NAME = $(subst ",,$(name))
FILENAME = $(MIGRATIONS_DIR)/$(TIMESTAMP)_$(NAME).py
LOWERCASE_NAME = $(shell echo $(name) | tr '[:upper:]' '[:lower:]')

.PHONY: migrate

## Create a new migration: make migrate name="create_users"
migrate_create:
	@mkdir -p $(MIGRATIONS_DIR)
	@touch $(FILENAME)
	@echo "from db.connection import dbConnection\n\nclient = dbConnection()\n\ndef up():\n    pass\n\ndef down():\n    pass" > $(FILENAME)
	@echo "Created $(FILENAME)"

## Apply migrations: make migrate-apply direction=up
migrate:
	@python -m db.migrate up

migrate_down:
	@python -m db.migrate down

## Copy target tenant credentials to env: set_env name="biopharma|kmh|wake|dev"
set_env:
	@cp .env.$(LOWERCASE_NAME) .env
	@docker compose down && docker compose up -d
	@echo "Set environment to $(LOWERCASE_NAME)"
