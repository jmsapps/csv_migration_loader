MIGRATIONS_DIR = db/migrations
TIMESTAMP = $(shell date +%Y%m%d%H%M%S)
NAME = $(subst ",,$(name))
FILENAME = $(MIGRATIONS_DIR)/$(TIMESTAMP)_$(NAME).py

.PHONY: migrate

## Create a new migration: make migrate name="create_users"
migrate_create:
	@mkdir -p $(MIGRATIONS_DIR)
	@touch $(FILENAME)
	@echo "from connection import dbConnection\n\nclient = dbConnection()\n\ndef up():\n    pass\n\ndef down():\n    pass" > $(FILENAME)
	@echo "Created $(FILENAME)"

## Apply migrations: make migrate-apply direction=up
migrate:
	@python db/migrate.py up

migrate_down:
	@python db/migrate.py down
