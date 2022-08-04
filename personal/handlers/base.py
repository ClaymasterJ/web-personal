"""Base handlers for the Tornado web server."""

# Core Libs
import inspect
import json
import re
import sys
import time
import uuid
import logging
from collections import defaultdict
from pathlib import Path

# Third-party libs
import tornado
import tornado.autoreload
import tornado.websocket

from tornado import gen
from tornado.ioloop import IOLoop, PeriodicCallback

# Source libs
from ..helpers import get_path_from_name
from ..constants import PATH_INFO, PATH_TEMPLATES


class HandlerWebsocket(tornado.websocket.WebSocketHandler):
    "Only one of these should be instanciated at a time"

    count = 0

    @gen.coroutine
    def open(self):
        self.application.addWebsocket(self)
        logging.info("WebSocket opened [_]")
        self.chirp()

    @gen.coroutine
    def chirp(self):
        logging.info("CAW")
        """Send message to client to update."""
        self.write_message("chirp")

    # @gen.coroutine
    # def on_message(self, message):
    #     # logging.info(source = self, message = "[RECIEVED] {}".format(message))
    #
    #     cargo = Cargo.loadData(message)
    #
    #     logging.info(source = self, message = "[RECIEVED] {}".format(cargo.__repr__()))
    #
    #     return self.send(self.application.parse(cargo, self))

    def on_close(self):
        logging.info("WebSocket closed [X]")

    # @gen.coroutine
    # def send(self, cargo):
    #     try:
    #         assert(isinstance(cargo, Cargo))
    #     except AssertionError:
    #         print(type(cargo))
    #         quit()
    #     self.write_message(cargo.wrap())
    #     logging.info(source = self, message = "[SENT] {}".format(repr(cargo)))


class HandlerPage(tornado.web.RequestHandler):
    "Base class for request handlers"

    @gen.coroutine
    def get(self, *args, **kwargs):

        self.render(
            get_path_from_name(
                name="_".join(self.__class__.__name__.split("_")[1:]),
                path=PATH_TEMPLATES,
            ).name,
            **self.__class__.variables()
        )

    @classmethod
    def variables(cls) -> dict:
        "Method to be overrided with varibles to pass into template"
        return {}

    @classmethod
    def title(cls):
        return " ".join(cls.__name__.split("_")[1:]).lower()

    @classmethod
    def url_local(cls):
        return "/" + "/".join(cls.__name__.lower().split("_")[1:])

    def raiseError(self, error):
        """Set the error and re-load the page."""
        self.error = error
        self.get()

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            return PH_Unauthorized.get()

        super().write_error(status_code, **kwargs)

    def initialize(self):
        """Set variables for PH."""
        # self.ModelHandler = (
        #     ModelHandler()
        # )  # TODO: Add ip or some identifying factor to the start of the ModelHandler object
        self.error = None

    @gen.coroutine
    def chirp(self):
        return self.application.chirp(self.user)


class HandlerAPI(HandlerPage):
    @classmethod
    def url_local(cls):
        return "/api{}".format(super().url_local())
