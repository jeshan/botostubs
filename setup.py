import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="botostubs",
    version="0.0.1",
    author="Jeshan G. BABOOA",
    author_email="j@jeshan.co",
    description="Stubs for boto3, the AWS SDK for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeshan/botostubs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD-2-Clause License",
        "Operating System :: OS Independent",
    ],
)
