from abjad.tools.abctools.Immutable import Immutable


class ImmutableDictionary(dict, Immutable):
    '''.. versionadded:: 2.0
    
    Immutable dictionary.

    The class disallows item set and item deletion after initialization.
    '''

    pass
