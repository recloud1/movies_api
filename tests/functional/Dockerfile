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

RUN echo "pytest ./src" > ./run_module.sh

ENTRYPOINT ["/bin/bash", "./run_module.sh"]