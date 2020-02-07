FROM python:3.6-alpine

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev tree curl

WORKDIR /app

RUN pip install pipenv

COPY Pipfile* ./

RUN pipenv install --system

RUN pip install --upgrade boto3

COPY test-data test-data
COPY post-release-data.py test_pytestcleanup_cases.py conftest.py pythonic.py main.py release.sh README.md setup.py ./

ENV AWS_DEFAULT_REGION=us-east-1

RUN export AWS_ACCESS_KEY_ID=FAKE AWS_SECRET_ACCESS_KEY=FAKE && \
  pytest --cov-report term-missing --cov=main -vv -s --show-progress test_pytestcleanup_cases.py

RUN mkdir -p botostubs/botostubs

RUN cp -r test_pytestcleanup_cases.py conftest.py setup.py README.md release.sh botostubs/
RUN touch botostubs/botostubs/py.typed
RUN export AWS_ACCESS_KEY_ID=FAKE AWS_SECRET_ACCESS_KEY=FAKE && time python main.py > botostubs/botostubs/__init__.py

WORKDIR botostubs
ENTRYPOINT ["./release.sh"]
