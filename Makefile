# Define required macros here
SHELL = /bin/sh

build:
	docker-compose build

build-nc:
	docker-compose build --no-cache

start:
	docker-compose up

exec-app:
	docker exec -it teklabs_test_task_app_1 sh

exec-db:
	docker exec -it teklabs_test_task_db_1 sh

exec-web:
	docker exec -it teklabs_test_task_web_1 sh

test:
	docker-compose run --rm app sh -c "python manage.py test"
