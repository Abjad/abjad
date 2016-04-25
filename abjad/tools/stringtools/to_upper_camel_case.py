# -*- coding: utf-8 -*-


def to_upper_camel_case(string):
    r'''Changes `string` to upper camel case.

    ..  container:: example

        Changes words to upper camel case:

        ::

            >>> stringtools.to_upper_camel_case('scale degrees 4 and 5')
            'ScaleDegrees4And5'

    ..  container:: example

        Changes snake case to upper camel case:

        ::

            >>> stringtools.to_upper_camel_case('scale_degrees_4_and_5')
            'ScaleDegrees4And5'

    ..  container:: example

        Changes dash case to upper camel case:

        ::

            >>> stringtools.to_upper_camel_case('scale-degrees-4-and-5')
            'ScaleDegrees4And5'

    ..  container:: example

        Changes upper camel case to upper camel case:

        ::

            >>> stringtools.to_upper_camel_case('ScaleDegrees4And5')
            'ScaleDegrees4And5'

    Returns string.
    '''
    from abjad.tools import stringtools
    words = stringtools.delimit_words(string)
    words = [_.capitalize() for _ in words]
    result = ''.join(words)
    return result
