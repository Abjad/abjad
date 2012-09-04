import types


def all_are_components_in_same_parent(expr, klasses=None, allow_orphans=True):
    '''.. versionadded:: 1.1

    True when elements in `expr` are all components in same parent.  Otherwise false::

        >>> staff = Staff(notetools.make_notes([12, 14, 16], [(1, 8)]))
        >>> componenttools.all_are_components_in_same_parent(staff.leaves)
        True

    True when elements in `expr` are all `klasses` in same parent. Otherwise false::

        >>> staff = Staff(notetools.make_notes([12, 14, 16], [(1, 8)]))
        >>> componenttools.all_are_components_in_same_parent(staff.leaves, klasses=(Note, ))
        True

    Return boolean.
    '''
    from abjad.tools import componenttools

    if not isinstance(expr, (list, tuple, types.GeneratorType)):
        #raise TypeError('must be list of components: "%s".' % str(expr))
        return False

    if klasses is None:
        klasses = (componenttools.Component, )
    else:
        klasses = tuple(klasses)

    if len(expr) == 0:
        return True

    first = expr[0]
    if not isinstance(first, klasses):
        return False

    first_parent = first._parent
    if first_parent is None and not allow_orphans:
        return False

    for element in expr[1:]:
        if not isinstance(element, klasses):
            return False
        if element._parent is not first_parent:
            return False

    return True
