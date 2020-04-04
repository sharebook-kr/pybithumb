import functools
import inspect
import warnings


class PyBithumbWraning(UserWarning):
    pass


def deprecated(instructions):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            message = 'Call to deprecated function {}. {}'.format(
                func.__name__,
                instructions)
            frame = inspect.currentframe().f_back
            warnings.warn_explicit(message,
                                   category=PyBithumbWraning,
                                   filename=inspect.getfile(frame.f_code),
                                   lineno=frame.f_lineno)
            return func(*args, **kwargs)
        return wrapper
    return decorator
