import abc


class AbjadObject(object, metaclass=abc.ABCMeta):
    """
    Abstract base class from which many custom classes inherit.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __format__(self, format_specification='') -> str:
        """
        Formats Abjad object.

        Set ``format_specification`` to ``''`` or ``'storage'``.
        Interprets ``''`` equal to ``'storage'``.
        """
        from .StorageFormatManager import StorageFormatManager
        if format_specification in ('', 'storage'):
            return StorageFormatManager(self).get_storage_format()
        return str(self)

    def __getstate__(self) -> dict:
        """
        Gets state of Abjad object.
        """
        if hasattr(self, '__dict__') and hasattr(vars(self), 'copy'):
            state = vars(self).copy()
        else:
            state = {}
        for class_ in type(self).__mro__:
            for slot in getattr(class_, '__slots__', ()):
                try:
                    state[slot] = getattr(self, slot)
                except AttributeError:
                    pass
        return state

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        from .StorageFormatManager import StorageFormatManager
        return StorageFormatManager(self).get_repr_format()

    def __setstate__(self, state) -> None:
        """
        Sets state of Abjad object.
        """
        for key, value in state.items():
            setattr(self, key, value)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        from .FormatSpecification import FormatSpecification
        return FormatSpecification(client=self)
