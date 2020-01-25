#!/usr/bin/env sh
set -ex

python setup.py sdist bdist_wheel
cp -r dist /custom

python -c "print('Sanity check'); import botostubs; print('Sanity check successful');" && twine upload --skip-existing --username ${TWINE_USERNAME} \
  --password ${TWINE_PASSWORD} dist/*

python ../post-release-data.py > data.json

curl --header "Content-Type: application/json" \
  -u jeshan:${GITHUB_TOKEN} \
  --request POST \
  --data @data.json \
  https://api.github.com/repos/jeshan/botostubs/releases
