from functools import wraps
from typing import Callable

from requests import Response

from exceptions import NoConnectionException


def check_status_code(
    code: int, msg: str = "Unexpected status code"
) -> Callable[..., Callable[..., Response]]:
    """
    Decorator that check if request was with an expected status code that
    passed to the decorator as an argument

    :param code: excepted status code
    :param msg: message of exception
    :return: result of the function
    """

    def ret_fun(func: Callable[..., Response]) -> Callable[..., Response]:
        @wraps(func)
        def inner(*args, **kwargs):
            response = func(*args, **kwargs)
            if response.status_code != code:
                raise NoConnectionException(msg)
            return response

        return inner

    return ret_fun
