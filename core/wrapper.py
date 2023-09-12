import threading

from functools import wraps


def async_func(func):
    """
    Thread Decorator

    Run the function in asynchronous
    """
    @wraps(func)
    def _wrapper_view(*args, **kwargs):
        thread = threading.Thread(
            target=func,
            name='Thread-async',
            args=args,
            kwargs=kwargs
        )
        thread.start()

    return _wrapper_view
