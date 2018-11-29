#!/usr/bin/env sh

python setup.py sdist bdist_wheel
cp -r dist /custom

python -c "print('Sanity check'); import botostubs; print('Sanity check successful');" && twine upload --username `aws ssm get-parameter --name /CodeBuild/pypi-user --output text --query Parameter.Value` \
  --password `aws ssm get-parameter --name /CodeBuild/pypi-password --output text --query Parameter.Value` dist/*
