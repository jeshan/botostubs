ARG TARGET_VERSION

FROM python:3.7-alpine

ENV AWS_ACCESS_KEY_ID=FAKE AWS_SECRET_ACCESS_KEY=FAKE AWS_DEFAULT_REGION=us-east-1

WORKDIR /app

RUN pip install pytest boto3 setuptools wheel

COPY main.py pythonic.py ./
COPY setup.py README.md botostubs/

RUN time python main.py > botostubs/__init__.py

RUN python -m pip install -e ./botostubs

RUN cd botostubs && python setup.py sdist bdist_wheel
