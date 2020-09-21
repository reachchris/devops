DOCKER_IMAGE=eu.gcr.io/ingka-sandbox-angup2-dev/deployer-demo/cricket-api
ENVIRONMENT ?= dev

.PHONY: build
build:
	docker build -t $(DOCKER_IMAGE) .

.PHONY: gcp-publish
gcp-publish: 
	docker tag ${DOCKER_IMAGE} ${DOCKER_IMAGE}:latest-$(ENVIRONMENT)
	docker push ${DOCKER_IMAGE}:latest-$(ENVIRONMENT)

.PHONY: publish
publish: build
	make gcp-publish