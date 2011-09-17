from _format_lilypond_value import _format_lilypond_value


def _format_lilypond_context_setting_inline(name, value, context = None):
    name = name.split('_')
    first = name[0:1]
    rest = name[1:]
    rest = [x.title() for x in rest]
    name = first + rest
    name = ''.join(name)
    value = _format_lilypond_value(value)
    if context is not None:
        context_string = context[1:]
        context_string = context_string.split('_')
        context_string = [x.title() for x in context_string]
        context_string = ''.join(context_string)
        context_string += '.'
    else:
        context_string = ''
    return r'\set %s%s = %s' % (context_string, name, value)
