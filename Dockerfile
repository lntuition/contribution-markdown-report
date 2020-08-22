FROM python:3.8.5-buster

LABEL maintainter "ekffu200098@gmail.com"

# Github actions doesn't recommend to use workdir in dockerfile. So should set workdir env to image.
# https://docs.github.com/en/actions/creating-actions/dockerfile-support-for-github-actions
ENV INPUT_WORKDIR "/workdir"
ENV PYTHONPATH "$PYTHONPATH:${INPUT_WORKDIR}"

COPY requirement.txt .
RUN pip install -r requirement.txt

COPY src ${INPUT_WORKDIR}
# Copied entrypoint.sh doesn't have execution permission
# entrypoint script must be LF format, at windows default format is CRLF and it makes me suck :(
RUN chmod +x ${INPUT_WORKDIR}/entrypoint.sh
ENTRYPOINT ["/workdir/entrypoint.sh"]
