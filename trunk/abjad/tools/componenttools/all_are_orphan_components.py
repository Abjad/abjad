from abjad.tools.componenttools.is_orphan_component import is_orphan_component


def all_are_orphan_components(expr):
    '''.. versionadded:: 2.0

    True when `expr` is an iterable of zero or more orphan components.

    Othewise false.
    '''

    for element in expr:
        if not is_orphan_component(element):
            return False
    else:
        return True
