ARG TARGET_VERSION

FROM python:3.6-alpine

ENV AWS_DEFAULT_REGION=us-east-1

WORKDIR /app

RUN pip install pytest boto3 setuptools wheel twine awscli

COPY main.py pythonic.py ./
COPY setup.py README.md release.sh botostubs/

RUN mkdir botostubs/botostubs
RUN export AWS_ACCESS_KEY_ID=FAKE AWS_SECRET_ACCESS_KEY=FAKE && time python main.py > botostubs/botostubs/__init__.py

WORKDIR /app/botostubs
CMD ./release.sh
