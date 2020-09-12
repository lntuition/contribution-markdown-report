FROM python:3.8.5-buster

LABEL maintainter "ekffu200098@gmail.com"

# https://docs.github.com/en/actions/creating-actions/dockerfile-support-for-github-actions#workdir
ENV ARTIFACT_PATH "/github/workspace/artifact"
ENV SOURCE_PATH "/action/src"
ENV REPO_PATH "/action/repo"
ENV PYTHONPATH "$PYTHONPATH:${SOURCE_PATH}"

COPY config ${SOURCE_PATH}
RUN pip install -r ${SOURCE_PATH}/requirement.txt
COPY src ${SOURCE_PATH}

# https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action#writing-the-action-code
ENTRYPOINT ["/action/src/script/entrypoint.sh"]
