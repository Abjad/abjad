# -*- coding: utf-8 -*-
import six
from abjad.tools.stringtools.strip_diacritics import strip_diacritics


def to_accent_free_snake_case(string):
    '''Changes `string` to accent-free snake case.

    ..  container:: example

        ::

            >>> stringtools.to_accent_free_snake_case('Déja vu')
            'deja_vu'

    Strips accents from accented characters.

    Changes all punctuation (including spaces) to underscore.

    Sets to lowercase.

    Returns string.
    '''
    assert isinstance(string, six.string_types)
    result = strip_diacritics(string)
    result = result.replace(' ', '_')
    result = result.replace("'", '_')
    result = result.lower()
    return result
