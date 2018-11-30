import boto3
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="botostubs",
    version="0.4." + boto3.__version__,
    author="Jeshan G. BABOOA",
    author_email="j@jeshan.co",
    description="Stubs for boto3, the AWS SDK for python",
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
