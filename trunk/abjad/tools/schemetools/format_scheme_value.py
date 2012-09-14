def format_scheme_value(value, force_quotes=False):
    '''Format `value` as Scheme would:

    ::
        
        >>> schemetools.format_scheme_value(1)
        '1'
    
    ::

        >>> schemetools.format_scheme_value('foo')
        'foo'

    ::

        >>> schemetools.format_scheme_value('bar baz')
        '"bar baz"'

    ::

        >>> schemetools.format_scheme_value([1.5, True, False])
        '(1.5 #t #f)'

    Strings without whitespace can be forcibly quoted via the `force_quotes` keyword:

    ::

        >>> schemetools.format_scheme_value('foo', force_quotes=True)
        '"foo"'

    Return string.
    '''
    from abjad.tools import schemetools

    if isinstance(value, str):
        value = value.replace('"', r'\"')
        if -1 == value.find(' ') and not force_quotes:
            return value
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
