
DOCKER_REPO ?= azman0101
DOCKER_NAME := docker-grafana-backup-tool
DOCKER_TAG ?= latest
PLATFORMS ?= linux/amd64,linux/arm/v7

FULLTAG = $(DOCKER_REPO)/$(DOCKER_NAME):$(DOCKER_TAG)

DOCKERFILE=Dockerfile

all: build

build:
	docker build -t $(FULLTAG) -f $(DOCKERFILE) .

push: build
	docker push $(FULLTAG)


buildx_and_push:
	docker buildx build \
		--output type=image,name=$(DOCKER_REPO)/$(DOCKER_NAME),push=true \
	 	--platform linux/amd64,linux/arm/v7 \
		--tag $(FULLTAG) \
	 	--file $(DOCKERFILE) .
