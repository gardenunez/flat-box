.PHONY:build shell test clean run create-app push
build:
	docker-compose build

shell: build
	docker-compose run --rm web /bin/bash

run: build
	docker-compose up

test: build
	docker-compose run --rm web bash -c "./db_scripts/prepare_db.sh && mamba tests -f documentation"

create-heroku-app: build
	heroku create flat-box --region eu
	heroku addons:create heroku-postgresql:hobby-dev
	heroku container:push web

build-heroku-image:
	docker build -t registry.heroku.com/flat-box/web .

push-heroku-image:
	docker push registry.heroku.com/flat-box/web

destroy-heroku-app:
	heroku apps:destroy flat-box

deploy: build-heroku-image push-heroku-image

clean:
	docker-compose stop && docker-compose rm -f
