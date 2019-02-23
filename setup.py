import os

import boto3
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="botostubs",
    version=os.environ['CODE_VERSION'] + "." + boto3.__version__,
    author="Jeshan G. BABOOA",
    author_email="j@jeshan.co",
    description="boto3 code assistance for any API in any IDE, always up to date",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeshan/botostubs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
