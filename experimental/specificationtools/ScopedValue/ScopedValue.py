from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.HorizontalScope import HorizontalScope


class ScopedValue(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, value, scope=None):
        assert isinstance(scope, (HorizontalScope, type(None)))
        self.value = value
        self.scope = scope 
