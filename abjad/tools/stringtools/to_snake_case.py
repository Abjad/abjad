# -*- coding: utf-8 -*-


def to_snake_case(string):
    r'''Changes `string` to snake case.

    ..  container:: example

        Changes words to snake case:

        ::

            >>> stringtools.to_snake_case('scale degrees 4 and 5')
            'scale_degrees_4_and_5'

    ..  container:: example

        Changes snake case to snake case:

        ::

            >>> stringtools.to_snake_case('scale_degrees_4_and_5')
            'scale_degrees_4_and_5'

    ..  container:: example

        Changes dash case to snake case:

        ::

            >>> stringtools.to_snake_case('scale-degrees-4-and-5')
            'scale_degrees_4_and_5'

    ..  container:: example

        Changes snake case to snake case:

        ::

            >>> stringtools.to_snake_case('ScaleDegrees4And5')
            'scale_degrees_4_and_5'

    Returns string.
    '''
    from abjad.tools import stringtools
    words = stringtools.delimit_words(string)
    words = [_.lower() for _ in words]
    result = '_'.join(words)
    return result
