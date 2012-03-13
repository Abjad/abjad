from abjad.tools.abctools import AbjadObject


class DoublingIndicator(AbjadObject):
    '''.. versionadded:: 2.0

    Indicator of chord doubling.

    Value object that can not be changed after instantiation.
    '''

    __slots__ = ('_doublings', )

    def __init__(self, doublings):
        object.__setattr__(self, '_doublings', doublings)

    ### PUBLIC PROPERTIES ###

    @property
    def doublings(self):
        return self._doublings
