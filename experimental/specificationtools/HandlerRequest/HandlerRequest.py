from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.handlers.Handler import Handler


class HandlerRequest(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, handler, offset=None):
        assert isinstance(handler, Handler)
        assert isinstance(offset, (int, type(None)))
        self.handler = handler
        self.offset = offset
