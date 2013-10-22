# -*- encoding: utf-8 -*-
import unicodedata


def strip_diacritics_from_binary_string(binary_string):
    r'''Strip diacritics from `binary_string`:

    ::

        >>> binary_string = 'Dvo\xc5\x99\xc3\xa1k'

    ::

        >>> print binary_string
        Dvořák

    ::

        >>> stringtools.strip_diacritics_from_binary_string(binary_string)
        'Dvorak'

    Returns ASCII string.
    '''

    unicode_string = unicode(binary_string, 'utf-8')
    normalized_unicode_string = unicodedata.normalize('NFKD', unicode_string)
    ascii_string = normalized_unicode_string.encode('ascii', 'ignore')

    return ascii_string
