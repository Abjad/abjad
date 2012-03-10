def list_checks():
    '''.. versionadded:: 2.8

    List checks.
    '''
    from abjad import checks
    
    result = []
    for name in dir(checks):
        if not name == 'Check':
            if name[0].isupper():
                exec('check = checks.{}()'.format(name))
                result.append(check)
    return result
