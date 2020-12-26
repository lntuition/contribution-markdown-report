CONTAINER_HOME = /action
HOST_HOME = ${CURDIR}/contribution-markdown-report
IMAGE = contribution-markdown-report-docker-image

# docker run [options] image [command] [arg ...]
define __docker_run
	docker run $(1) ${IMAGE} $(2)
endef

entrypoint = --entrypoint ""
user = --user $(shell id -u):$(shell id -g)
volume = --volume ${HOST_HOME}:${CONTAINER_HOME}
workdir = --workdir ${CONTAINER_HOME}

# build
build:
	docker build -t ${IMAGE} .
build-no-cache:
	docker build -t ${IMAGE} . --no-cache
build-clean:
	docker rmi -f ${IMAGE}

# clean
clean:
	sudo rm -rf ${CURDIR}/output

# debug
debug: build
	$(call __docker_run, \
		${entrypoint} \
		${workdir} \
		--interactive \
		--tty \
		, \
		bash \
	)

# isort
isort: build
	$(call __docker_run, \
		${entrypoint} \
		${user} \
		${workdir} \
		, \
		isort --check-only --diff \
		${CONTAINER_HOME} \
	)

isort-fix: build
	$(call __docker_run, \
		${entrypoint} \
		${user} \
		${volume} \
		${workdir} \
		, \
		isort \
		${CONTAINER_HOME} \
	)

# black
black: build
	$(call __docker_run, \
		${entrypoint} \
		${user} \
		${workdir} \
		, \
		black --check --diff \
		${CONTAINER_HOME} \
	)

black-fix: build
	$(call __docker_run, \
		${entrypoint} \
		${user} \
		${volume} \
		${workdir} \
		, \
		black \
		${CONTAINER_HOME} \
	)

# pylint: temporary disabled with pylint issue
pylint: build
ifeq (0, 1)
	$(call __docker_run, \
		${entrypoint} \
		${user} \
		${workdir} \
		, \
		pylint \
		${CONTAINER_HOME}/src \
		${CONTAINER_HOME}/main.py \
	)
endif

# mypy
mypy: build
	$(call __docker_run, \
		${entrypoint} \
		${user} \
		${workdir} \
		, \
		mypy \
		${CONTAINER_HOME}/src \
		${CONTAINER_HOME}/main.py \
	)

# unit
unit: build
	$(call __docker_run, \
		${entrypoint} \
		${workdir} \
		, \
		python -m pytest --cov=src --cov-report=term-missing \
	)

unit-codecov: build
	$(call __docker_run, \
		${entrypoint} \
		${workdir} \
		--volume ${CURDIR}/output:/output \
		, \
		python -m pytest --cov=src --cov-report=term-missing --cov-report=xml:/output/coverage.xml \
	)

# integration
integration: build
	$(call __docker_run, \
		--workdir /github/workspace \
		-e INPUT_WORKSPACE=result \
		-e INPUT_FILE_NAME=README \
		-e INPUT_USER=lntuition \
		-e INPUT_START_DATE=2018-01-01 \
		-e INPUT_END_DATE=yesterday \
		-e INPUT_LANGUAGE=english \
		-e INPUT_REMOTE=https://github.com/lntuition/empty-archive \
		-e INPUT_LOCAL=/output \
		--volume ${CURDIR}/output:/output \
		, \
	)
