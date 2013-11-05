# -*- encoding: utf-8 -*-
from abjad.tools import stringtools


def make_lilypond_revert_string(
    grob_name, 
    grob_attribute, 
    context_name=None,
    ):
    '''Makes LilyPond revert string.

    Returns string.
    '''
    from abjad.tools import formattools

    # parse input strings
    grob_name = stringtools.snake_case_to_upper_camel_case(grob_name)
    grob_attribute = formattools.LilyPondFormatManager.format_lilypond_attribute(
        grob_attribute)

    # change #'bound-details #'left #'text to #'bound-details
    grob_attribute = grob_attribute.split(' ')[0]

    context_prefix = ''
    if context_name is not None:
        context_prefix = \
            stringtools.snake_case_to_upper_camel_case(context_name)
        context_prefix += '.'

    # format revert string
    result = r'\revert {}{} {}'
    result = result.format(context_prefix, grob_name, grob_attribute)
    
    # return revert string
    return result
