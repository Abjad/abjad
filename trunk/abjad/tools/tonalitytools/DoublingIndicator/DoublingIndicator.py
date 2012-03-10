from abjad.tools.abctools import Immutable


class DoublingIndicator(Immutable):
    '''.. versionadded:: 2.0

    Indicator of chord doubling.

    Value object that can not be changed after instantiation.
    '''

    def __init__(self, doublings):
        object.__setattr__(self, '_doublings', doublings)

    ### PUBLIC ATTRIBUTES ###

    @property
    def doublings(self):
        return self._doublings
