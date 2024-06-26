help:
	@echo "usage: make <target>"
	@echo "Targets:"
	@echo "	build"
	@echo "	up"
	@echo " up_detach"
	@echo "	down"
	@echo "	destroy"
	@echo "	stop"
	@echo "	up_test"
	@echo "	down_test"
	@echo "	build_image_app"

build:
	docker-compose -f docker-compose.yml  build
up_detach:
	docker-compose -f docker-compose.yml  up -d
up:
	docker-compose -f docker-compose.yml  up
stop:
	docker-compose -f docker-compose.yml  stop
down:
	docker-compose -f docker-compose.yml  down
destroy:
	docker-compose -f docker-compose.yml  down -v
up_test:
    docker-compose -f docker-compose-tests.yml up
down_test:
    docker-compose -f docker-compose-tests.yml down -v
build_image_app:
     docker build -t sprint5 -f dockerization/Dockerfile .
build_image_tests:
     docker build -t sprint5-tests -f dockerization/Dockerfile-test .
