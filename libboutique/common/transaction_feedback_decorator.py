import logging
from typing import Dict, Any, Tuple
from functools import wraps

from libboutique.common.transaction_actions import TransactionActionsEnum


def format_glib_error(exception) -> Dict:
    return {"args": exception.args, "code": exception.code, "domain": exception.domain, "message": exception.message}


def successful_message(action: TransactionActionsEnum, arguments: Tuple, result: Any) -> Dict:
    return {"action": action, "arguments": arguments, "message": "success", "result": result}


class transaction_feedback_decorator:
    """
        ******************************
        *        **DECORATOR**       *
        ******************************

        Unify the response structure for every service
        supported
    """

    def __init__(self, action: TransactionActionsEnum):
        self.action = action.value

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                fn(*args, **kwargs)
                logging.info(f"Success: {self.action} - {args} & {kwargs}")
                return successful_message(action=self.action, arguments=(args, kwargs))
            except Exception as ex:
                logging.exception(f"Error: {self.action} - {args} & {kwargs}: {ex}")
                return format_glib_error(exception=ex)

        return wrapper
