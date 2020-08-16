FROM python:3.8.5-buster

LABEL maintainter "ekffu200098@gmail.com"

ENV DEFAULT_DIR /actions
RUN mkdir -p ${DEFAULT_DIR}

COPY requirement.txt ${DEFAULT_DIR}
RUN pip install -r ${DEFAULT_DIR}/requirement.txt

COPY src ${DEFAULT_DIR}
ENV PYTHONPATH "$PYTHONPATH:${DEFAULT_DIR}"
RUN chmod +x ${DEFAULT_DIR}/entrypoint.sh

ENTRYPOINT ["/actions/entrypoint.sh"]
