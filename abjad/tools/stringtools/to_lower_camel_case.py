# -*- coding: utf-8 -*-


def to_lower_camel_case(string):
    r'''Changes `string` to lower camel case.

    ..  container:: example

        Changes words to lower camel case:

        ::

            >>> stringtools.to_lower_camel_case('scale degrees 4 and 5')
            'scaleDegrees4And5'

    ..  container:: example

        Changes snake case to lower camel case:

        ::

            >>> stringtools.to_lower_camel_case('scale_degrees_4_and_5')
            'scaleDegrees4And5'

    ..  container:: example

        Changes dash case to lower camel case:

        ::

            >>> stringtools.to_lower_camel_case('scale-degrees-4-and-5')
            'scaleDegrees4And5'

    ..  container:: example

        Changes upper camel case to lower camel case:

        ::

            >>> stringtools.to_lower_camel_case('ScaleDegrees4And5')
            'scaleDegrees4And5'

    Returns string.
    '''
    from abjad.tools import stringtools
    result = stringtools.to_upper_camel_case(string)
    if result == '':
        return result
    result = result[0].lower() + result[1:]
    return result
