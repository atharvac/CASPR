

help:
	@echo "\ninstall\t: installs python packages from requirements.txt"
	@echo "run\t: runs flask application"
	@echo "db-init\t: initialize database"
	@echo "db-up\t: upgrades database revision"
	@echo "db-down\t: downgrades database revision"
	@echo "test\t: run pytest\n"


install:
	@echo "Installing Packages from requirements.txt"
	pip install -r requirements.txt

run:
	flask run

db-init:
	flask db init

db-up:
	flask db upgrade

db-down:
	flask db downgrade

test:
	pytest