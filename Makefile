envPath=./.env
current_date = $(shell date +%Y%m%d_%H%M%S)
ccache:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -exec rm -f {} +
	find . -type f -name "*.pyo" -exec rm -f {} +
r:
	./.venv/bin/pip install -r requirements.txt
venv:
	python3.12 -m venv .venv
build:
	docker-compose build
	# --no-cache 
run:
	docker-compose up -d
down:
	docker-compose down --rmi all
stop:
	docker-compose stop

