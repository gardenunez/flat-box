.PHONY:build shell test clean run
build:
	docker-compose build
shell: build
	docker-compose run --rm api /bin/bash

run: build
	docker-compose run --rm api

test:
	docker-compose run --rm -e --no-deps api bash -c "mamba tests -f documentation"

clean:
	docker-compose stop && docker-compose rm -f
