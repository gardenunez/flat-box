.PHONY:build shell test clean
build:
	docker-compose build
shell: build
	docker-compose build

run: build
	docker-compose run api bash -c 'FLASK_APP=app.py flask run'

clean:
	docker-compose stop && docker-compose rm -f
