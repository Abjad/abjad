import types


def all_are_components_in_same_thread(expr, klasses=None, allow_orphans=True):
    '''.. versionadded:: 1.1

    True when elements in `expr` are all components in same thread. Otherwise false::

        >>> voice = Voice("c'8 d'8 e'8")
        >>> componenttools.all_are_components_in_same_thread(voice.leaves)
        True

    True when elements in `expr` are all `klasses` in same thread. Otherwise false::

        >>> voice = Voice("c'8 d'8 e'8")
        >>> componenttools.all_are_components_in_same_thread(voice.leaves, klasses=Note)
        True

    Return boolean.
    '''
    from abjad.tools import componenttools

    if not isinstance(expr, (list, tuple, types.GeneratorType)):
        #raise TypeError('Must be list of Abjad components.')
        return False

    if klasses is None:
        klasses = componenttools.Component

    if len(expr) == 0:
        return True

    first = expr[0]
    if not isinstance(first, klasses):
        return False

    orphan_components = True
    if not componenttools.is_orphan_component(first):
        orphan_components = False

    same_thread = True

    first_signature = componenttools.component_to_containment_signature(first)
    for component in expr[1:]:
        if not componenttools.is_orphan_component(component):
            orphan_components = False
        if componenttools.component_to_containment_signature(component) != first_signature:
            same_thread = False
        if not allow_orphans and not same_thread:
            return False
        if allow_orphans and not orphan_components and not same_thread:
            return False

    return True
