from abjad.tools.abctools.AbjadObject import AbjadObject


class StatalServerRequest(AbjadObject):

    ### INITIALIZER ###
    
    def __init__(self, server, count=None, offset=None):
        from experimental import specificationtools
        assert isinstance(server, specificationtools.StatalServer)
        self.server = server
        self.count = count
        self.offset = offset

    ### SPECIAL METHODS ###

    def __call__(self):
        return self.server(self)
