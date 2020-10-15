FROM python:3.8.5-buster

# https://docs.github.com/en/actions/creating-actions/dockerfile-support-for-github-actions
# https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action
LABEL maintainter "ekffu200098@gmail.com"

# Python
RUN pip install beautifulsoup4 gitpython requests seaborn tabulate \
        black freezegun isort mypy pylint pytest pytest-cov

# Setup
COPY contribution-markdown-report /action
ENTRYPOINT ["python", "/action/main.py"]
