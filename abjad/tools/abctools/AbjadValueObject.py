from .AbjadObject import AbjadObject


class AbjadValueObject(AbjadObject):
    r'''Abstract base class for classes which compare equally based on their
    storage format.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments):
        r'''Copies Abjad value object.

        Returns new Abjad value object.
        '''
        import abjad
        return abjad.new(self)

    def __eq__(self, argument):
        r'''Is true when all initialization values of Abjad value object equal
        the initialization values of `argument`.

        Returns true or false.
        '''
        import abjad
        return abjad.TestManager.compare_objects(self, argument)

    def __hash__(self):
        r'''Hashes Abjad value object.

        Returns integer.
        '''
        from abjad.tools import systemtools
        hash_values = systemtools.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            message = 'unhashable type: {}'.format(self)
            raise TypeError(message)
        return result
