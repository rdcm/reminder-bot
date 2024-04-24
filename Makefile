activate:
	echo 'activate manually: python3 -m venv venv && source venv/bin/activate && source .env'

install:
	pip install poetry && poetry install

format:
	black .

lint:
	pylint -rn ./src/**/*.py

run:
	python src/reminder_bot/main.py

docker-build:
	docker build --no-cache -t reminder_bot .

docker-run:
	docker run -e BOT_TOKEN=$(BOT_TOKEN) -e PYTHONUNBUFFERED=TRUE -d reminder_bot

deactivate:
	echo 'deactivate manually: deactivate'