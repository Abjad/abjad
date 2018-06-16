def list_all_classes(modules=None, ignored_classes=None):
    r'''Lists all public classes defined in `path`.

    ..  container:: example

        ::

            >>> all_classes = abjad.utilities.list_all_classes(
            ...     modules='abjad',
            ...     )

    '''
    from abjad import utilities
    all_classes = set()
    for module in utilities.yield_all_modules(modules):
        name = module.__name__.split('.')[-1]
        if name.startswith('_'):
            continue
        if not hasattr(module, name):
            continue
        obj = getattr(module, name)
        if isinstance(obj, type):
            all_classes.add(obj)
    if ignored_classes:
        ignored_classes = set(ignored_classes)
        all_classes.difference_update(ignored_classes)
    return list(sorted(
        all_classes,
        key=lambda x: (x.__module__, x.__name__)
        ))
