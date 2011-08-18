from _format_lilypond_value import _format_lilypond_value


def _format_lilypond_context_setting_in_with_block(name, value):
    name = name.split('_')
    first = name[0:1]
    rest = name[1:]
    rest = [x.title() for x in rest]
    name = first + rest
    name = ''.join(name)
    value = _format_lilypond_value(value)
    return r'%s = %s' % (name, value)
