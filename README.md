[![PyPI version](https://badge.fury.io/py/botostubs.svg)](https://badge.fury.io/py/botostubs)

![Build badge](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiUzdpbkQ3WHQxTkVWVWhvQ2tZVGVZMUJNcC9KYzFQZGFYOGtuOXVmc0tTdkYwNWlEM3dCNjQwSkZqTlhZZWVxZGk3V1l6VFdwU3piSlQxaHArUmJkdTFjPSIsIml2UGFyYW1ldGVyU3BlYyI6InFMQjZObmxqQWJ0ZXpVUHoiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)


# botostubs
Gives you code assistance for **any boto3 API** in any IDE. Get started by running `pip install botostubs`


# Demo
![See demo gif on github](https://raw.githubusercontent.com/jeshan/botostubs/master/intro-demo.gif)


# Features
- show required / optional fields
- full api coverage

# How it works
We look for all boto3 clients by running boto itself. Then loop over each of them to find what operations and classes are used. These are all dumped in a new python script, packaged in this project. This way, `botostubs` can offer comprehensive API coverage.

# TODO
Support python versions before 3.5. Currently requires at least 3.5 due to use of type hints.

# Credits
`pyboto3` for inspiration behind this. It supported only legacy Python and not Python 3. Besides, it is no longer being maintained.

# Releasing on pypi
- `docker-compose build`
- `docker-compose run python`. Enter credentials when prompted
