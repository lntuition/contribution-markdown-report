FROM python:3.8.5-buster

LABEL maintainter "ekffu200098@gmail.com"

# Github actions doesn't recommend to use workdir in dockerfile. So should set workdir env to image.
# https://docs.github.com/en/actions/creating-actions/dockerfile-support-for-github-actions
ENV INPUT_WORKDIR "/workdir"
ENV PYTHONPATH "$PYTHONPATH:${INPUT_WORKDIR}"

COPY config ${INPUT_WORKDIR}
RUN pip install -r ${INPUT_WORKDIR}/requirement.txt
COPY src ${INPUT_WORKDIR}

# Copied entrypoint.sh doesn't have execution permission
# entrypoint script must be LF format, at windows default format is CRLF and it makes me suck :(
RUN chmod -R +x ${INPUT_WORKDIR}/script
ENTRYPOINT ["/workdir/script/entrypoint.sh"]
