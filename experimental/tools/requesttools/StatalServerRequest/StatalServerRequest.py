from experimental.tools import statalservertools
from experimental.tools.requesttools.Request import Request


class StatalServerRequest(Request):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental.tools import *

    Request `statal_server`.

    Apply any of `index`, `count` that are not none.

    The purpose of a statal server request is to function as the source of a setting.
    '''

    ### INITIALIZER ###
    
    def __init__(self, statal_server, modifications=None, index=None, count=None):
        assert isinstance(server, statalservertools.StatalServer)
        Request.__init__(self, modifications=modifications, index=index, count=count)
        self._statal_server = statal_server

    ### SPECIAL METHODS ###

    def __call__(self):
        return self.statal_server(self)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def statal_server(self):
        return self._statal_server
