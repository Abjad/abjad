from abjad.tools import stringtools


# TODO: make public and move somewhere
def _make_lilypond_revert_string(grob_name, grob_attribute, context_name=None):
    '''.. versionadded:: 2.0

    Make LilyPond revert string.
    '''
    from _format_lilypond_attribute import _format_lilypond_attribute
    from _format_lilypond_value import _format_lilypond_value

    # parse input strings
    grob_name = stringtools.underscore_delimited_lowercase_to_uppercamelcase(grob_name)
    grob_attribute = _format_lilypond_attribute(grob_attribute)
    if context_name is not None:
        context_prefix = stringtools.underscore_delimited_lowercase_to_uppercamelcase(context_name)
        context_prefix += '.'
    else:
        context_prefix = ''

    # return override string
    return r'\revert %s%s %s' % (context_prefix, grob_name, grob_attribute)
