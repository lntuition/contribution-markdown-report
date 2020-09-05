WORKDIR="/workdir"
IMAGE="contribution-markdown-report"

build:
	docker build -t ${IMAGE} .

clean:
	docker rmi -f ${IMAGE}

debug: build
	docker run -it --workdir ${WORKDIR} --entrypoint "" ${IMAGE} bash

pytest:
	docker run -it --workdir ${WORKDIR} --entrypoint "" ${IMAGE} pytest
mypy:
	docker run -it --workdir ${WORKDIR} --entrypoint "" ${IMAGE} mypy
test: build pytest mypy
