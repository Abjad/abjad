from abjad.system.AbjadObject import AbjadObject


class AbjadValueObject(AbjadObject):
    """
    Abstract base class for classes which compare equally based on their
    storage format.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        from .StorageFormatManager import StorageFormatManager
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        from .StorageFormatManager import StorageFormatManager
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f'unhashable type: {self}')
        return result
