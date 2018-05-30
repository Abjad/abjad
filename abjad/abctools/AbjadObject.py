import abc


class AbjadObject(object, metaclass=abc.ABCMeta):
    """
    Abstract base class from which many custom classes inherit.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        """
        Formats Abjad object.

        Set ``format_specification`` to ``''`` or ``'storage'``.
        Interprets ``''`` equal to ``'storage'``.

        Returns string.
        """
        import abjad
        if format_specification in ('', 'storage'):
            return abjad.StorageFormatManager(self).get_storage_format()
        return str(self)

    def __getstate__(self):
        """
        Gets state of Abjad object.

        Returns dictionary.
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

    def __repr__(self):
        """
        Gets interpreter representation of Abjad object.

        Returns string.
        """
        import abjad
        return abjad.StorageFormatManager(self).get_repr_format()

    def __setstate__(self, state):
        """
        Sets state of Abjad object.

        Returns none.
        """
        for key, value in state.items():
            setattr(self, key, value)

    ### PRIVATE METHODS ###

    def _debug(self, value, annotation=None, blank=False):
        if annotation is None:
            print('debug: {!r}'.format(value))
        else:
            print('debug ({}): {!r}'.format(annotation, value))
        if blank:
            print()

    def _debug_values(self, values, annotation=None, blank=True):
        if values:
            for value in values:
                self._debug(value, annotation=annotation)
            if blank:
                print()
        else:
            self._debug(repr(values), annotation=annotation)
            if blank:
                print()

    def _get_format_specification(self):
        import abjad
        return abjad.FormatSpecification(client=self)
