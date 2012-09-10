from experimental import timespaninequalitytools
from experimental.requesttools.Request import Request


class CommandRequest(Request):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Request `attribute` active at `timepoint` in `context_name`.

    The instruction pointed to by this request is canonically assumed
    to be a list or other iterable that can or will be read as a statal server.

    Because of this the request also affords several list-manipulation attributes.
    These are `callback`, `count`, `offset`, `reverse`.

    The purpose of an instruction request is to function as the source of a setting.

    This implementation is currently a stub.
    '''

    ### INITIALIZER ###

    def __init__(self, attribute, timepoint,
        context_name=None, callback=None, count=None, offset=None, reverse=None):
        assert attribute in self.attributes, repr(attribute)
        assert isinstance(timepoint, timepointtools.Timepoint)
        assert isinstance(context_name, (str, type(None))), repr(context_name)
        Request.__init__(self, callback=callback, count=count, offset=offset, reverse=reverse)
        self._attribute = attribute
        self._timepoint = timepoint
        self._context_name = context_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        return self._attribute

    @property
    def context_name(self):
        return self._context_name

    @property
    def segment_identifier(self):
        '''Delegate to ``self.timepoint.segment_identifier``.
        '''
        return self.timepoint.segment_identifier

    @property
    def timepoint(self):
        return self._timepoint
