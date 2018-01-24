# Mozilla AutoPush Load-Tester

FROM python:3.5-slim

MAINTAINER Richard Pappalardo <rpappalardo@mozilla.com>

RUN mkdir -p /home/autograph-loadtest
ADD . /home/autograph-loadtest

WORKDIR /home/autograph-loadtest

RUN \
    BUILD_DEPS="git build-essential" && \
    RUN_DEPS="wget libssl-dev" && \
    apt-get update && \
    apt-get install -yq --no-install-recommends ${BUILD_DEPS} ${RUN_DEPS} && \
    pip install virtualenv && \
    virtualenv -p `which python3` venv && \
    ./venv/bin/pip install -r requirements.txt && \
    apt-get purge -yq --auto-remove ${BUILD_DEPS} && \
    apt-get autoremove -qq && \
    apt-get clean -y
# End run

#CMD ["./venv/bin/molotov", "./loadtest.py", "-w ${WORKERS}"]
CMD ./venv/bin/molotov ./loadtest.py -w ${WORKERS} -d ${DURATION} -p ${PROCESSES} ${VERBOSE}

