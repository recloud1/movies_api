FROM python:3.9

ENV PYTHONPATH=/var/testing

RUN mkdir -p $PYTHONPATH
WORKDIR $PYTHONPATH

COPY ./requirements.txt ./

RUN apt-get update  \
    && apt-get install -y --no-install-recommends  \
       netcat  \
       curl  \
    && pip install -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

# CUSTOM HEALTHCHECK
RUN echo "while ! curl elasticsearch:9200; do sleep 1; done;" > ./run_module.sh \
&& echo "until ((printf "AUTH $TEST_REDIS_PASSWORD\r\n"; sleep 1) | nc redis 6379); do echo waiting for redis; sleep 2; done" > ./run_module.sh \
&& echo "pytest ./src" > ./run_module.sh

ENTRYPOINT ["/bin/bash", "./run_module.sh"]