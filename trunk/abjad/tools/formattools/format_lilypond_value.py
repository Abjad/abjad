# -*- encoding: utf-8 -*-


def format_lilypond_value(value):
    r'''Formats LilyPond value according to Scheme formatting conventions.

    Returns string.
    '''

    if 'lilypond_format' in dir(value) and not isinstance(value, str):
        return value.lilypond_format
    elif value is True:
        return '##t'
    elif value is False:
        return '##f'
    elif value is Up:
        return '#up'
    elif value is Down:
        return '#down'
    elif value is Left:
        return '#left'
    elif value is Right:
        return '#right'
    elif value is Center:
        return '#center'
    elif _is_lilypond_constant(value):
        return '#%s' % value
    elif _is_lilypond_function_name(value):
        return '#%s' % value
    elif isinstance(value, tuple):
        return "#'(%s . %s)" % value
    elif isinstance(value, str) and ' ' not in value:
        return "#'%s" % value
    elif isinstance(value, str) and ' ' in value:
        return '"%s"' % value
    else:
        return "#'%s" % value


def _is_lilypond_constant(value):
    r'''True if value is constant.  Otherwise false.
    '''

    if isinstance(value, int) or isinstance(value, float) or value in [
        'up', 'down', 'left', 'center', 'right',
        'black', 'white', 'red', 'green',
        'blue', 'cyan', 'magenta', 'yellow',
        'grey', 'darkred', 'darkgreen', 'darkblue',
        'darkcyan', 'darkmagenta', 'darkyellow', ]:
        return True
    else:
        return False


def _is_lilypond_function_name(arg):
    r'''True if arg contains '::'. Otherwise false.
    '''

    return isinstance(arg, str) and '::' in arg
