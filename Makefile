.PHONY:build shell test clean
build:
	docker-compose build
shell: build
	docker-compose run --rm --service-ports flat_box_api /bin/bash

test: build
	docker-compose run --rm flat_box_api bash -c 'FLASK_APP=app.py flask run'

clean:
	docker-compose stop && docker-compose rm -f
