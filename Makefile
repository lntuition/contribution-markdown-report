WORKDIR="/workdir"
IMAGE="contribution-markdown-report"

build:
	docker build -t ${IMAGE} .
clean:
	docker rmi -f ${IMAGE}
debug: build
	docker run -it --workdir ${WORKDIR} --entrypoint "" ${IMAGE} bash
test: build
	docker run -it --workdir ${WORKDIR} --entrypoint "" ${IMAGE} pytest -v --cov=lib
