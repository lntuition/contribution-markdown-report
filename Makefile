IMAGE="contribution-markdown-report"

SOURCE="${CURDIR}/src"
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
black:
	docker run -it --workdir ${WORKDIR} --entrypoint "" -v ${SOURCE}/${CLIENT}:${WORKDIR}/${CLIENT} -v ${SOURCE}/${LIB}:${WORKDIR}/${LIB} ${IMAGE} black ${LIB} ${CLIENT}
pylint:
	docker run -it --workdir ${WORKDIR} --entrypoint "" ${IMAGE} pylint ${LIB} ${CLIENT}

test: build pytest mypy black pylint
