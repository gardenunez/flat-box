.PHONY:build shell test clean
build:
	docker-compose build
shell: build
	docker-compose build

run: build
	docker-compose run api

clean:
	docker-compose stop && docker-compose rm -f
