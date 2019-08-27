import logging
from functools import wraps


def format_glib_error(exception):
    return {"args": exception.args, "code": exception.code, "domain": exception.domain, "message": exception.message}


def successful_message(action, arguments):
    return {"action": action, "arguments": arguments, "message": "success"}


class TransactionFeedbackDecorator:
    def __init__(self, action):
        self.action = action

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                fn(*args, **kwargs)
                logging.info("Success: {self.action} - {args} & {kwargs}".format(**locals()))
                return successful_message(action=self.action, arguments=(args, kwargs))
            except Exception as ex:
                logging.exception("Error: {self.action} - {args} & {kwargs}: {ex}".format(**locals()))
                return format_glib_error(exception=ex)

        return wrapper
