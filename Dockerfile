FROM python:3.8.5-buster

# https://docs.github.com/en/actions/creating-actions/dockerfile-support-for-github-actions
# https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action
LABEL maintainter "ekffu200098@gmail.com"

# Environment
ENV OUTPUT_PATH "/github/workspace"
ENV HOME_PATH "/action"

# Python
RUN pip install beautifulsoup4 requests seaborn gitpython \
        black freezegun isort mypy pylint pytest pytest-cov
ENV PYTHONPATH "$PYTHONPATH:${HOME_PATH}/src"

# Setup
COPY contribution-markdown-report ${HOME_PATH}
ENTRYPOINT ["python", "/action/src/main.py"]
