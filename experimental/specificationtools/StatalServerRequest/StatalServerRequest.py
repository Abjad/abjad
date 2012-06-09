from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.StatalServer import StatalServer


class StatalServerRequest(AbjadObject):

    ### INITIALIZER ###
    
    def __init__(self, server, count=None, offset=None):
        assert isinstance(server, StatalServer)
        self.server = server
        self.count = count
        self.offset = offset

    ### SPECIAL METHODS ###

    def __call__(self):
        return self.server(self)
