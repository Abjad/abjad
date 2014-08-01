# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class AbjadValueObject(AbjadObject):
    r'''Abstract base class for classes which compare equally based on their
    storage format.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when all initialization values of Abjad value object equal
        the initialization values of `expr`.

        Returns boolean.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __hash__(self):
        r'''Hashes Abjad value object.

        Returns integer.
        '''
        from abjad.tools import systemtools
        return hash(systemtools.StorageFormatManager.get_hash_values(self))