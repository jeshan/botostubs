#!/usr/bin/env sh

python setup.py sdist bdist_wheel
cp -r dist /custom

python -c "print('Sanity check'); import botostubs; print('Sanity check successful');" && twine upload --username ${TWINE_USERNAME} \
  --password ${TWINE_PASSWORD} dist/*
