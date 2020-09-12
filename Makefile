IMAGE = "contribution-markdown-report"

HOST_SOURCEPATH = "${CURDIR}/src"
CONTAINER_SOURCEPATH = "/action/src"

LIB_DIR = "lib"
CLIENT_DIR = "client"

VOLUME_LIB = "${CONTAINER_SOURCEPATH}/${LIB_DIR}:/${HOST_SOURCEPATH}/${LIB_DIR}"
VOLUME_CLIENT = "${CONTAINER_SOURCEPATH}/${CLIENT_DIR}:/${HOST_SOURCEPATH}/${CLIENT_DIR}"

build:
	docker build -t ${IMAGE} .

clean:
	docker rmi -f ${IMAGE}

debug: build
	docker run -it \
	--workdir ${CONTAINER_SOURCEPATH} \
	--entrypoint "" \
	${IMAGE} \
	bash

test_isort:
	docker run \
	--workdir ${CONTAINER_SOURCEPATH} \
	--entrypoint "" \
	${IMAGE} \
	isort --check-only ${LIB_DIR} ${CLIENT_DIR}
test_black:
	docker run \
	--workdir ${CONTAINER_SOURCEPATH} \
	--entrypoint "" \
	${IMAGE} \
	black --check ${LIB_DIR} ${CLIENT_DIR}
test_pylint:
	docker run \
	--workdir ${CONTAINER_SOURCEPATH} \
	--entrypoint "" \
	${IMAGE} \
	pylint ${LIB_DIR} ${CLIENT_DIR}
test_mypy:
	docker run \
	--workdir ${CONTAINER_SOURCEPATH} \
	--entrypoint "" \
	${IMAGE} \
	mypy ${LIB_DIR} ${CLIENT_DIR}
test_pytest:
	docker run \
	--workdir ${CONTAINER_SOURCEPATH} \
	--entrypoint "" \
	${IMAGE} \
	pytest --cov=${LIB_DIR}
test: build test_isort test_black test_pylint test_mypy test_pytest
	
style_isort:
	docker run \
	--workdir ${CONTAINER_SOURCEPATH} \
	--entrypoint "" \
	--volume ${VOLUME_LIB}} \
	--volume ${VOLUME_CLIENT} \
	${IMAGE} \
	isort ${LIB_DIR} ${CLIENT_DIR}
style_black:
	docker run \
	--workdir ${CONTAINER_SOURCEPATH} \
	--entrypoint "" \
	--volume ${VOLUME_LIB}} \
	--volume ${VOLUME_CLIENT} \
	${IMAGE} \
	black ${LIB_DIR} ${CLIENT_DIR}
style: build style_isort style_black
