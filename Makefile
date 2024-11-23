dev-install:
	pip install -r dev.requirements.txt

lint:
	flake8 .
	mypy .

fmt:
	isort .
	black .

run:
	python3 main.py

test:
	.
