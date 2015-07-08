[![Coverage Status](https://coveralls.io/repos/wtelecom/net-interviewer/badge.svg?branch=master&service=github)](https://coveralls.io/github/wtelecom/net-interviewer?branch=master)
[![Code Health](https://landscape.io/github/wtelecom/net-interviewer/master/landscape.svg?style=flat)](https://landscape.io/github/wtelecom/net-interviewer/master)


# net-interviewer
Tool to send request and get network information


# [coveralls.io](https://coveralls.io)

To run coverall test create a `.coveralls.yml` file at the root level:

    repo_token: abcdef1234569abdcef
    service_name: travis-pro
    parallel: true # if the CI is running your build in parallel

Then run:

    coverage run --source=interviewer test/runTests.py
