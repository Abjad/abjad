# -*- coding: utf-8 -*-


def to_dash_case(string):
    r'''Changes `string` to dash case.

    ..  container:: example

        Changes words to dash case:

        ::

            >>> stringtools.to_dash_case('scale degrees 4 and 5')
            'scale-degrees-4-and-5'

    ..  container:: example

        Changes snake case to dash case:

        ::

            >>> stringtools.to_dash_case('scale_degrees_4_and_5')
            'scale-degrees-4-and-5'

    ..  container:: example

        Changes dash case to dash case:

        ::

            >>> stringtools.to_dash_case('scale-degrees-4-and-5')
            'scale-degrees-4-and-5'

    ..  container:: example

        Changes upper camel case to dash case:

        ::

            >>> stringtools.to_dash_case('ScaleDegrees4And5')
            'scale-degrees-4-and-5'

    Returns string.
    '''
    from abjad.tools import stringtools
    words = stringtools.delimit_words(string)
    words = [_.lower() for _ in words]
    result = '-'.join(words)
    return result
