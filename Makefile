# Constant setting
HOST_HOME_PATH = ${CURDIR}/contribution-markdown-report
CONTAINER_HOME_PATH = /action

# Docker setting
IMAGE_DEFAULT = contribution-markdown-report
WORKDIR_DEFAULT= --workdir ${CONTAINER_HOME_PATH}
ENTRYPOINT_DEFAULT = --entrypoint ""
VOLUME_DEFAULT = --volume ${HOST_HOME_PATH}:${CONTAINER_HOME_PATH}
VOLUME_OUTPUT = --volume ${CURDIR}/output:/github/workspace

# Function
DOCKER_RUN = docker run ${1} ${IMAGE_DEFAULT}

# Setup
build:
	docker build -t ${IMAGE_DEFAULT} .

# Cleanup
clean:
	docker rmi -f ${IMAGE_DEFAULT}

# Debug
DEBUG_OPTION = ${WORKDIR_DEFAULT} ${ENTRYPOINT_DEFAULT}  --interactive --tty
DEBUG_BASE = $(call DOCKER_RUN, ${DEBUG_OPTION})
debug: build
	${DEBUG_BASE} bash

# Test
TEST_OPTION = ${WORKDIR_DEFAULT} ${ENTRYPOINT_DEFAULT}
TEST_BASE = $(call DOCKER_RUN, ${TEST_OPTION})
test-isort:
	${TEST_BASE} isort --check-only --diff ${CONTAINER_HOME_PATH}
test-black:
	${TEST_BASE} black --check --diff ${CONTAINER_HOME_PATH}
test-pylint:
	${TEST_BASE} pylint ${CONTAINER_HOME_PATH}
test-mypy:
	${TEST_BASE} mypy ${CONTAINER_HOME_PATH}
test-pytest:
	${TEST_BASE} pytest --cov=src
test: build test-isort test-black test-pylint test-mypy test-pytest

# Style
STYLE_OPTION = ${WORKDIR_DEFAULT} ${ENTRYPOINT_DEFAULT} ${VOLUME_DEFAULT}
STYLE_BASE = $(call DOCKER_RUN, ${STYLE_OPTION})
style-isort:
	${STYLE_BASE} isort ${CONTAINER_HOME_PATH}
style-black:
	${STYLE_BASE} black ${CONTAINER_HOME_PATH}
style: build style-isort style-black
