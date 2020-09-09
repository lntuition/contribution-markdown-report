# Common settings
IMAGE = "contribution-markdown-report" 

LIB_DIR = "lib"
CLIENT_DIR = "client"
TEST_DIR = "test"

# Host settings
HOST_WORKDIR_PATH = "${CURDIR}/src"
HOST_LIB_PATH = "${HOST_WORKDIR_PATH}/${LIB_DIR}"
HOST_CLIENT_PATH = "${HOST_WORKDIR_PATH}/${CLIENT_DIR}"

# Container settings
CONTAINER_WORKDIR_PATH = "/workdir"
CONTAINER_LIB_PATH = "${CONTAINER_WORKDIR_PATH}/${LIB_DIR}"
CONTAINER_CLIENT_PATH = "${CONTAINER_WORKDIR_PATH}/${CLIENT_DIR}"

build:
	docker build -t ${IMAGE} .

clean:
	docker rmi -f ${IMAGE}

debug: build
	docker run -it \
	--workdir ${CONTAINER_WORKDIR_PATH} \
	--entrypoint "" \
	${IMAGE} \
	bash

test_isort:
	docker run \
	--workdir ${CONTAINER_WORKDIR_PATH} \
	--entrypoint "" \
	${IMAGE} \
	isort --check-only ${LIB_DIR} ${CLIENT_DIR}
test_black:
	docker run \
	--workdir ${CONTAINER_WORKDIR_PATH} \
	--entrypoint "" \
	${IMAGE} \
	black --check ${LIB_DIR} ${CLIENT_DIR}
test_pylint:
	docker run \
	--workdir ${CONTAINER_WORKDIR_PATH} \
	--entrypoint "" \
	${IMAGE} \
	pylint ${LIB_DIR} ${CLIENT_DIR}
test_mypy:
	docker run \
	--workdir ${CONTAINER_WORKDIR_PATH} \
	--entrypoint "" \
	${IMAGE} \
	mypy ${LIB_DIR} ${CLIENT_DIR}
test_pytest:
	docker run \
	--workdir ${CONTAINER_WORKDIR_PATH} \
	--entrypoint "" \
	${IMAGE} \
	pytest ${TEST_DIR} --cov=${LIB_DIR}

test: build test_isort test_black test_pylint test_mypy test_pytest
	
style_isort:
	docker run \
	--workdir ${CONTAINER_WORKDIR_PATH} \
	--entrypoint "" \
	--volume ${HOST_LIB_PATH}:${CONTAINER_LIB_PATH} \
	--volume ${HOST_CLIENT_PATH}:${CONTAINER_CLIENT_PATH} \
	${IMAGE} \
	isort ${LIB_DIR} ${CLIENT_DIR}
style_black:
	docker run \
	--workdir ${CONTAINER_WORKDIR_PATH} \
	--entrypoint "" \
	--volume ${HOST_LIB_PATH}:${CONTAINER_LIB_PATH} \
	--volume ${HOST_CLIENT_PATH}:${CONTAINER_CLIENT_PATH} \
	${IMAGE} \
	black ${LIB_DIR} ${CLIENT_DIR}

style: build style_isort style_black
