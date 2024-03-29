include .env

.PHONY: run install installdev format

run:
	cd app && poetry run uvicorn main:app --host $(SERVER_ADDR) --port $(SERVER_PORT)

install:
	poetry install

installdev:
	poetry install --with dev

format:
	isort ./app
	black ./app --line-length 79
	flake8 ./app