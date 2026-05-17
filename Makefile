.PHONY: build docker-push minikube-deploy switch-blue switch-green test

IMAGE_NAME=aceest-fitness-api
TAG=staging

build:
	docker build -t $(IMAGE_NAME):$(TAG) .

docker-push:
	@echo "Provide DOCKER_USER as environment variable, e.g. DOCKER_USER=me make docker-push"
	@if [ -z "$(DOCKER_USER)" ]; then \
		echo "DOCKER_USER not set"; exit 1; \
	fi
	docker tag $(IMAGE_NAME):$(TAG) $(DOCKER_USER)/$(IMAGE_NAME):$(TAG)
	docker push $(DOCKER_USER)/$(IMAGE_NAME):$(TAG)

minikube-deploy:
	./scripts/deploy_minikube.sh $(DOCKER_USER)/$(IMAGE_NAME):$(TAG)

switch-blue:
	./scripts/switch_bluegreen.sh blue

switch-green:
	./scripts/switch_bluegreen.sh green

test:
	/Users/varshagajula/Desktop/bits-pilani/semester3/ACEest-Fitness-and-Gym-Devops/venv/bin/python -m pytest -q
