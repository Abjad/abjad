# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class AbjadValueObject(AbjadObject):
    r'''Abstract base class for classes which compare equally based on their
    storage format.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies Abjad value object.

        Returns new Abjad value object.
        '''
        specification = self._storage_format_specification
        positional_arguments = specification.positional_argument_values
        keyword_arguments = {}
        for name in specification.keyword_argument_names:
            keyword_arguments[name] = getattr(self, name)
        return type(self)(*positional_arguments, **keyword_arguments)

    def __eq__(self, expr):
        r'''Is true when all initialization values of Abjad value object equal
        the initialization values of `expr`.

        Returns true or false.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __hash__(self):
        r'''Hashes Abjad value object.

        Returns integer.
        '''
        from abjad.tools import systemtools
        hash_values = systemtools.StorageFormatManager.get_hash_values(self)
        try:
            result = hash(hash_values)
        except TypeError:
            message = 'unhashable type: {}'.format(self)
            raise TypeError(message)
        return result
