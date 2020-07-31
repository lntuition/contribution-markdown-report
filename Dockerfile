FROM python:3.8.5-buster

LABEL maintainter "ekffu200098@gmail.com"

RUN pip install beautifulsoup4 matplotlib pytablewriter[all] requests
RUN git clone https://github.com/lntuition/daily-contribution-checker.git /actions
RUN chmod +x /actions/src/entrypoint.sh
ENTRYPOINT ["/actions/src/entrypoint.sh"]
