.PHONY: help
help:
	@echo
	@echo 'Available commands:'
	@echo '  init:  Create initial database and super user'
	@echo

.PHONY: init
init:
	python3 manage.py migrate
	python3 manage.py loaddata traits.json booking_types.json
	python3 manage.py createsuperuser

.PHONY: get_columns
get_columns:
	@for x in $$(sqlite3 data/db.sqlite3 '.tables base_%'); do \
		echo; echo "=== $$x ==="; \
		sqlite3 data/db.sqlite3 "PRAGMA table_info($$x)" | cut -d'|' -f1-2; \
	done
