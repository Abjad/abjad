from abjad.tools.abctools.Immutable import Immutable


class ImmutableDictionary(dict, Immutable):
    '''.. versionadded:: 2.0
    
    Immutable dictionary::

        abjad> from abjad.tools import datastructuretools

    ::

        abjad> dictionary = datastructuretools.ImmutableDictionary({'color': 'red', 'number': 9})

    ::

        abjad> dictionary
        {'color': 'red', 'number': 9}

    ::

        abjad> dictionary['color']
        'red'

    ::

        abjad> dictionary.size = 'large'
        AttributeError: ImmutableDictionary objects are immutable.

    ::

        abjad> dictionary['size'] = 'large'
        AttributeError: ImmutableDictionary objects are immutable.

    Return immutable dictionary.
    '''

    ### OVERLOADS ###

    def __delitem__(self, *args):
        raise AttributeError('{} objects are immutable.'.format(self._class_name))

    def __setitem__(self, *args):
        raise AttributeError('{} objects are immutable.'.format(self._class_name))
