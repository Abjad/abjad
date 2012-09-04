def all_are_orphan_components(expr):
    '''.. versionadded:: 2.0

    True when `expr` is an iterable of zero or more orphan components.

    Othewise false.
    '''
    from abjad.tools import componenttools

    for element in expr:
        if not componenttools.is_orphan_component(element):
            return False
    else:
        return True
