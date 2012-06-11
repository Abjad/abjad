from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.TemporalScope import TemporalScope


class ScopedValue(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, value, scope=None):
        assert isinstance(scope, (TemporalScope, type(None)))
        self.value = value
        self.scope = scope 
