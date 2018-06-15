from abjad.system.AbjadObject import AbjadObject


class AbjadValueObject(AbjadObject):
    """
    Abstract base class for classes which compare equally based on their
    storage format.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments):
        """
        Copies Abjad value object.

        Returns new Abjad value object.
        """
        import abjad
        return abjad.new(self)

    def __eq__(self, argument):
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.

        Returns true or false.
        """
        import abjad
        return abjad.TestManager.compare_objects(self, argument)

    def __hash__(self):
        """
        Hashes Abjad value object.

        Returns integer.
        """
        from abjad import system
        hash_values = system.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f'unhashable type: {self}')
        return result
