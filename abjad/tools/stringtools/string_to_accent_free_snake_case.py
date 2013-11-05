# -*- encoding: utf-8 -*-
from abjad.tools.stringtools.strip_diacritics_from_binary_string \
	import strip_diacritics_from_binary_string


def string_to_accent_free_snake_case(string):
    '''Change `string` to strict directory name:

    ::

        >>> stringtools.string_to_accent_free_snake_case('Déja vu')
        'deja_vu'

    Strip accents from accented characters.
    Change all punctuation (including spaces) to underscore.
    Set to lowercase.

    Returns string.
    '''

    assert isinstance(string, str)

    result = strip_diacritics_from_binary_string(string)
    result = result.replace(' ', '_')
    result = result.replace("'", '_')
    result = result.lower()

    return result
