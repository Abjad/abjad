def format_scheme_value(value):
    '''Format `value` as Scheme would:

    ::
        
        abjad> from abjad.tools.schemetools import format_scheme_value
        abjad> format_scheme_value(1)
        '1'
        abjad> format_scheme_value('foo bar')
        '"foo bar"'
        abjad> format_scheme_value([1.5, True, False])
        '(1.5 #t #f)'

    Return string.
    '''
    from abjad.tools import schemetools

    if isinstance(value, str):
        if -1 == value.find(' ') and -1 == value.find('"'):
            return value
        elif value.startswith('"') and value.endswith('"'):
            return value
        else:
            return '"{}"'.format(value)

    elif isinstance(value, bool):
        if value:
            return '#t'
        return '#f'

    elif isinstance(value, (list, tuple)):
        return '(%s)' % ' '.join([format_scheme_value(x) for x in value])

    elif isinstance(value, schemetools.Scheme):
        return str(value)

    elif isinstance(value, type(None)):
        return '#f'

    return str(value)
