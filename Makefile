activate:
	python3 -m venv venv && echo 'activate manually: source venv/bin/activate'

install:
	pip install poetry && poetry install

format:
	black .

lint:
	pylint -rn ./src/**/*.py

run:
	python3 src/reminder_bot/main.py

deactivate:
	echo 'deactivate manually: deactivate'