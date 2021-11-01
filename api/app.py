#!/bin/env python

from pluto_api import app


class BaseConfig(object):
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 5000


class Develop(BaseConfig):
    pass


if __name__ == '__main__':
    # create app run parameters
    dev = Develop()
    app.run(host=dev.HOST, port=dev.PORT, debug=dev.DEBUG)
