# -*- encoding: utf-8 -*-
from abjad.tools import stringtools


# TODO: make public and move to bound method of some class
def _make_lilypond_override_string(grob_name, grob_attribute, grob_value, context_name=None, is_once=False):
    '''Does not include once indicator.
    '''
    from _format_lilypond_attribute import _format_lilypond_attribute
    from _format_lilypond_value import _format_lilypond_value

    # parse input strings
    grob_name = stringtools.snake_case_to_upper_camel_case(grob_name)
    grob_attribute = _format_lilypond_attribute(grob_attribute)
    grob_value = _format_lilypond_value(grob_value)
    if context_name is not None:
        context_prefix = stringtools.snake_case_to_upper_camel_case(context_name)
        context_prefix += '.'
    else:
        context_prefix = ''
    if is_once:
        once_prefix = r'\once '
    else:
        once_prefix = ''

    # return override string
    return r'%s\override %s%s %s = %s' % (
        once_prefix, context_prefix, grob_name, grob_attribute, grob_value)
