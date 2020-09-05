IMAGE="contribution-markdown-report"
WORKDIR="/workdir"
LIB="lib"
CLIENT="main.py"

build:
	docker build -t ${IMAGE} .

clean:
	docker rmi -f ${IMAGE}

debug: build
	docker run -it --workdir ${WORKDIR} --entrypoint "" ${IMAGE} bash

pytest:
	docker run -it --workdir ${WORKDIR} --entrypoint "" ${IMAGE} pytest --cov=${LIB}
mypy:
	docker run -it --workdir ${WORKDIR} --entrypoint "" ${IMAGE} mypy ${LIB} ${CLIENT}
pylint:
	docker run -it --workdir ${WORKDIR} --entrypoint "" ${IMAGE} pylint ${LIB} ${CLIENT}
test: build pytest mypy pylint
