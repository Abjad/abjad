# -*- encoding: utf-8 -*-


# TODO: make public and move to bound method of some class
def _format_lilypond_context_setting_inline(name, value, context=None):
    from abjad.tools import formattools

    name = name.split('_')
    first = name[0:1]
    rest = name[1:]
    rest = [x.title() for x in rest]
    name = first + rest
    name = ''.join(name)
    value = formattools.format_lilypond_value(value)
    if context is not None:
        context_string = context[1:]
        context_string = context_string.split('_')
        context_string = [x.title() for x in context_string]
        context_string = ''.join(context_string)
        context_string += '.'
    else:
        context_string = ''

    result = r'\set {}{} = {}'
    result = result.format(context_string, name, value)

    return result
