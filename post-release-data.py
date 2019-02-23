#!/usr/bin/env python
import boto3
import os
print(f'{{"tag_name": "v{os.environ["CODE_VERSION"]}.{boto3.__version__}", "name": "{os.environ["CODE_VERSION"]}.{boto3.__version__}", "body": "Compatibility with boto3 version {boto3.__version__}"}}')

