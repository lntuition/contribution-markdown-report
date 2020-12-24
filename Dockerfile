FROM python:3.8.5-buster
LABEL maintainter "ekffu200098@gmail.com"

# Setup
RUN pip install \
        beautifulsoup4 \
        black \
        freezegun \
        isort \
        mypy \
        pylint \
        pytest \
        pytest-cov \
        responses \
        requests \
        seaborn \
        tabulate
# Source
COPY contribution-markdown-report /action

ENTRYPOINT ["/action/entrypoint.sh"]
