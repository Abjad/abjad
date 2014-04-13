# -*- encoding: utf-8 -*-
from abjad.tools.stringtools.strip_diacritics \
	import strip_diacritics


def to_accent_free_snake_case(string):
    '''Change `string` to strict directory name:

    ::

        >>> stringtools.to_accent_free_snake_case('Déja vu')
        'deja_vu'

    Strip accents from accented characters.
    Change all punctuation (including spaces) to underscore.
    Set to lowercase.

    Returns string.
    '''

    assert isinstance(string, str)

    result = strip_diacritics(string)
    result = result.replace(' ', '_')
    result = result.replace("'", '_')
    result = result.lower()

    return result