MIGRATIONS_DIR = db/migrations
TIMESTAMP = $(shell date +%Y%m%d%H%M%S)
NAME = $(subst ",,$(name))
FILENAME = $(MIGRATIONS_DIR)/$(TIMESTAMP)_$(NAME).py
LOWERCASE_NAME = $(shell echo $(name) | tr '[:upper:]' '[:lower:]')

.PHONY: migrate

## Create a new migration: make migrate_create name="create_users"
migrate_create:
	@mkdir -p $(MIGRATIONS_DIR)
	@touch $(FILENAME)
	@echo "from db.connection import dbConnection\n\nclient = dbConnection()\n\ndef up():\n    pass\n\ndef down():\n    pass" > $(FILENAME)
	@echo "Created $(FILENAME)"

## Apply migrations: make migrate
migrate:
	@python -m db.migrate up

## Rollback latest migration: make migrate_down
migrate_down:
	@python -m db.migrate down

## Check currently applied migration for target tenant: make migrate_current name="biopharma|kmh|wake|dev"
migrate_current:
	@if [ -s db/migrations/.current_$(LOWERCASE_NAME) ]; then \
		echo "Current migration for $(LOWERCASE_NAME) is $$(cat db/migrations/.current_$(LOWERCASE_NAME))"; \
	else \
		echo "No migrations for $(LOWERCASE_NAME) have been applied."; \
	fi

## Copy target tenant credentials to env: set_env name="biopharma|kmh|wake|dev"
set_env:
	@cp .env.$(LOWERCASE_NAME) .env
	@docker compose down && docker compose up -d
	@echo "Set environment to $(LOWERCASE_NAME)"
