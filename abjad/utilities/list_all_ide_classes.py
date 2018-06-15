def list_all_ide_classes(modules=None, ignored_classes=None):
    r'''Lists all public classes defined in Abjad IDE.

    ::

        >>> all_classes = utilities.list_all_ide_classes()  # doctest: +SKIP

    '''
    from abjad import utilities
    try:
        return utilities.list_all_classes(
            modules='ide',
            ignored_classes=ignored_classes,
            )
    except ImportError:
        return []
