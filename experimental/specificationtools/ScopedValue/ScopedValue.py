from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.Timespan import Timespan


class ScopedValue(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, value, scope=None):
        assert isinstance(scope, (Timespan, type(None)))
        self.value = value
        self.scope = scope 
