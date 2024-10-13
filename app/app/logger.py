import logging
from io import BytesIO

import msgpack
from fluent.handler import FluentRecordFormatter

from fluent import asynchandler

LOGGER_NAME = "uvicorn.fluent"


def overflow_handler(pendings):
    unpacker = msgpack.Unpacker(BytesIO(pendings))
    for unpacked in unpacker:
        print(unpacked)


class FluentLogger:
    def __init__(
        self,
        name=LOGGER_NAME,
        level=logging.DEBUG,
        disabled=False,
        propagate=False,
    ):
        self._logger: logging.Logger = logging.getLogger(name)
        self._logger.disabled = disabled
        self._logger.propagate = propagate
        self._logger.setLevel(level)

        self.handler = asynchandler.FluentHandler(
            tag="app.tcp.log",
            host="localhost",
            port=24224,
            buffer_overflow_handler=overflow_handler,
            verbose=True,
        )
        self.formatter = FluentRecordFormatter(
            {
                "host": "%(hostname)s",
                "where": "%(module)s.%(funcName)s",
                "type": "%(levelname)s",
                "stack_trace": "%(exc_text)s",
                "message": "%(message)s",
            }
        )
        self.handler.setFormatter(self.formatter)
        self.handler.setLevel(level)
        self._logger.addHandler(self.handler)
        self._logger.addHandler(logging.StreamHandler())

    def close(self):
        self.handler.close()
        print("AsyncHandler closed.")

