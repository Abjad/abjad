from experimental.tools import statalservertools
from experimental.tools.requesttools.Request import Request


class StatalServerRequest(Request):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental.tools import *

    Request `statal_server`.

    The purpose of a statal server request is to function as the source of a setting.
    '''

    ### INITIALIZER ###
    
    def __init__(self, statal_server, modifications=None):
        assert isinstance(server, statalservertools.StatalServer)
        Request.__init__(self, modifications=modifications)
        self._statal_server = statal_server

    ### SPECIAL METHODS ###

    def __call__(self):
        return self.statal_server(self)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def statal_server(self):
        return self._statal_server
