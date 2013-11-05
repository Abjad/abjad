# -*- encoding: utf-8 -*-
from abjad.tools import stringtools


def make_lilypond_override_string(
    grob_name,
    grob_attribute,
    grob_value,
    context_name=None,
    is_once=False,
    ):
    '''Makes Lilypond override string.

    Does not include once indicator.

    Returns string.
    '''
    from abjad.tools import formattools

    # parse input strings
    grob_name = stringtools.snake_case_to_upper_camel_case(grob_name)
    grob_attribute = formattools.LilyPondFormatManager.format_lilypond_attribute(
        grob_attribute)
    grob_value = formattools.LilyPondFormatManager.format_lilypond_value(grob_value)
    if context_name is not None:
        context_prefix = \
            stringtools.snake_case_to_upper_camel_case(context_name)
        context_prefix += '.'
    else:
        context_prefix = ''
    if is_once:
        once_prefix = r'\once '
    else:
        once_prefix = ''

    # return override string
    result = r'{}\override {}{} {} = {}'
    result = result.format(
        once_prefix,
        context_prefix,
        grob_name,
        grob_attribute,
        grob_value,
        )

    return result
