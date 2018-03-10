.PHONY:build shell test clean run
build:
	docker-compose build

shell: build
	docker-compose run --rm api /bin/bash

run: build
	docker-compose up

test: build
	docker-compose run --rm api bash -c "./prepare_db.sh && mamba tests -f documentation"

clean:
	docker-compose stop && docker-compose rm -f
