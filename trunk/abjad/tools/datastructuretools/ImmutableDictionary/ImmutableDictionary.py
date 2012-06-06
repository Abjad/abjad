from abjad.tools.abctools.AbjadObject import AbjadObject


class ImmutableDictionary(dict, AbjadObject):
    '''.. versionadded:: 2.0
    
    Immutable dictionary::

        >>> from abjad.tools import datastructuretools

    ::

        >>> dictionary = datastructuretools.ImmutableDictionary({'color': 'red', 'number': 9})

    ::

        >>> dictionary
        {'color': 'red', 'number': 9}

    ::

        >>> dictionary['color']
        'red'

    ::

        >>> dictionary.size = 'large' # doctest: +SKIP
        AttributeError: ImmutableDictionary objects are immutable.

    ::

        >>> dictionary['size'] = 'large' # doctest: +SKIP
        AttributeError: ImmutableDictionary objects are immutable.

    Return immutable dictionary.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __delitem__(self, *args):
        raise AttributeError('{} objects are immutable.'.format(self._class_name))

    def __setitem__(self, *args):
        raise AttributeError('{} objects are immutable.'.format(self._class_name))
