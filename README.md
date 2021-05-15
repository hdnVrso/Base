# Base
[![Build Status](https://travis-ci.org/hiddenSt/Base.svg?branch=master)](https://travis-ci.org/hiddenSt/Base)
[![Coverage Status](https://coveralls.io/repos/github/hiddenSt/Base/badge.svg?branch=master)](https://coveralls.io/github/hiddenSt/Base?branch=master)
## Prerequisites
Before you begin, ensure you have met the following requirements:
* Docker
* Docker-compose
* Python 3.8 or newer

## Using Base

To use Base, follow these steps:

* Build containers using following command
```Shell
docker-compose build
```
* Start containers
```Shell
docker-compose up -d
```
Now you can interract with app through `127.0.0.1:8000`

## Contributing to Base
To contribute to Base, follow these steps:
1. Fork this repository if you are not a collaborator
2. Create a branch: `git checkout -b <branch_name>`
3. Make your changes and commit them
4. Push your branch to the repository
5. Create the pull request

## Check code coverage locally
To check code coverage locally follow these steps:
1. Start up containers
```shell
docker-compose up -d
```
build images if you need:
```shell
docker-compose up -d --builld
```
2. Run shell in ``django`` container
```shell
docker-compose exec django /bin/ash
```
after this you must be in container shell

3. Run coverage.py to generate report
```shell
coverage run manage.py test
```
4. You can see report by executing the following:
```shell
coverage report
```
if you need more precise or detailed report see [coverage.py](https://coverage.readthedocs.io/en/coverage-5.5/cmd.html) docs.

<i>Note: we need 90% coverage for our code base. Improve only your codebase</i>

