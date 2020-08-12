![](https://img.shields.io/badge/programmer-laziness-green.svg)
[![PyPI version](https://badge.fury.io/py/botostubs.svg)](https://badge.fury.io/py/botostubs)

[![Downloads](https://pepy.tech/badge/botostubs)](https://pepy.tech/project/botostubs)
[![Downloads](https://pepy.tech/badge/botostubs/month)](https://pepy.tech/project/botostubs)
[![Downloads](https://pepy.tech/badge/botostubs/week)](https://pepy.tech/project/botostubs)

![Build badge](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiUkF6bllTcVBkQmI2Y0FWZlpDUTRHc3pyVm5EUk11ZWdDV1BtcVAyZG80TCtJZFZUdnB1ZmFwRVN3UWxudUJxMTRTTW15R1dnUy9KZFZuZE1Fd3c1b1RjPSIsIml2UGFyYW1ldGVyU3BlYyI6IlNZa3Q2aHRjWjVYVzQ0clkiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)


# botostubs
Gives you code assistance for **any boto3 API** in any IDE. Get started by running `pip install botostubs`


# Demo
![See demo gif on github](https://raw.githubusercontent.com/jeshan/botostubs/master/intro-demo.gif)


# Features
- PyPI package automatically aligned with boto3 (yay!)
- show required / optional fields
- show API docs as Python docstrings
- full api coverage
- support for boto3 clients, e.g `type: botostubs.ACM`
- support for service-level resources, e.g `type: botostubs.S3.S3Resource`
- support for paginators, e.g `type: botostubs.EC2.DescribeInstancesPaginator`
- support for waiters, e.g `type: botostubs.EC2.InstanceRunningWaiter`

# How it works
We look for all boto3 clients by running boto itself. Then loop over each of them to find what operations and classes are used. These are all dumped in a new python script, packaged in this project. This way, `botostubs` can offer comprehensive API coverage.

The deployment pipeline on AWS checks for boto3 releases every 3 days, installs it, generate new stubs and pushes them to PyPI. Looking for a new API released a few days ago? Just upgrade the package with `pip install --upgrade botostubs` and you're good to go.

For an in-depth account, see the blog post [Code assistance for boto3, always up to date and in any IDE](https://www.awsadvent.com/2018/12/21/code-assistance-for-boto3-always-up-to-date-and-in-any-ide/)

# Notes
- This package requires that your IDE already supports getting type hints from PyPI packages. It has been tested with Intellij and Visual Studio Code.
- If you are not seeing code completion in Intellij-based ones, please increase the intellisense filesize limit e.g `idea.max.intellisense.filesize=20000` in IDE custom properties (Help > Edit Custom Properties), then restart
- For other IDEs, you may have some luck by installing [jedi](https://github.com/davidhalter/jedi), which provides code completion for Vim, Emacs, Sublime, Atom, etc.

# TODO
Support python versions before 3.6. Currently requires at least 3.6 due to use of type hints.

# Credits
`pyboto3` for inspiration behind this. It supported only legacy Python and not Python 3. Besides, it is no longer being maintained.

# For forkers
## Automated releasing on pypi
Deploy the pipeline in your AWS account by clicking this button:
<a href="https://console.aws.amazon.com/cloudformation/home?#/stacks/new?&templateURL=https://s3.amazonaws.com/jeshan-oss-public-files/deployment-pipeline.yaml" target="_blank"><img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"></a>

This is how it looks like:

![stack](/stack.png)

*Image automatically generated with [cfnbuddy](https://www.cfnbuddy.com)*

## Manual Releasing on pypi
- `docker-compose build`
- `docker-compose run python`. Enter credentials when prompted
