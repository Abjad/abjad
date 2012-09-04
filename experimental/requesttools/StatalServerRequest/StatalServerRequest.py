from experimental import statalservertools
from experimental.requesttools.Request import Request


class StatalServerRequest(Request):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Request `statal_server`.
    Apply any of `callback`, `count`, `offset` that are not none.

    The purpose of a statal server request is to function as the source of a setting.
    '''

    ### INITIALIZER ###
    
    def __init__(self, statal_server, callback=None, count=None, offset=None):
        assert isinstance(server, statalservertools.StatalServer)
        Request.__init__(self, callback=callback, count=count, offset=offset)
        self.statal_server = statal_server

    ### SPECIAL METHODS ###

    def __call__(self):
        return self.statal_server(self)
