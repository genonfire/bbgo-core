import threading

from django.http import Http404
from django.shortcuts import _get_queryset

from utils.debug import Debug


def get_object_or_404(klass, *args, **kwargs):
    """
    For Debugging Convenience

    Same as Django's shortcut.
    Check django/shortcuts.py
    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, 'get'):
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__  # noqa
        raise ValueError(
            "First argument to get_object_or_404() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        Debug.trace(' No %s%s matches the given query.' % (
            queryset.model._meta.object_name, kwargs)
        )
        if not threading.current_thread().name == 'Thread-async':
            raise Http404('No %s matches the given query.' % queryset.model._meta.object_name)  # noqa
