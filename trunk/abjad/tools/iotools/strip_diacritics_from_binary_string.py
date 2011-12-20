# -*- encoding: utf-8 -*-
import unicodedata


def strip_diacritics_from_binary_string(binary_string):
    r'''.. versionadded:: 2.5

    Strip diacritics from `binary_string`::

        abjad> binary_string = 'Dvo\xc5\x99\xc3\xa1k'

    ::

        abjad> print binary_string
        Dvořák

    ::

        abjad> iotools.strip_diacritics_from_binary_string(binary_string)
        'Dvorak'

    Return ASCII string.
    '''

    unicode_string = unicode(binary_string, 'utf-8')
    normalized_unicode_string = unicodedata.normalize('NFKD', unicode_string)
    ascii_string = normalized_unicode_string.encode('ascii', 'ignore')

    return ascii_string
