def list_all_ide_functions(modules=None):
    r'''Lists all public functions defined in Abjad IDE.

    ::

        >>> all_functions = utilities.list_all_ide_functions()  # doctest: +SKIP

    '''
    from abjad import utilities
    try:
        return utilities.list_all_functions(modules='ide')
    except ImportError:
        return []
