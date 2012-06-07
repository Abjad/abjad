from abjad.tools.abctools.AbjadObject import AbjadObject
from specificationtools.Scope import Scope


class ScopedValue(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, value, scope=None):
        assert isinstance(scope, (Scope, type(None)))
        self.value = value
        self.scope = scope 
