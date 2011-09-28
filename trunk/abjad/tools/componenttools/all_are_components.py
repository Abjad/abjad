from abjad.tools.componenttools._Component import _Component
import types


def all_are_components(expr, klasses=None):
    '''.. versionadded:: 1.1

    True when elements in `expr` are all components::

        abjad> componenttools.all_are_components(3 * Note("c'4"))
        True

    Otherwise false::

        abjad> componenttools.all_are_components(['foo', 'bar'])
        False

    True when elements in `expr` are all `klasses`::

        abjad> componenttools.all_are_components(3 * Note("c'4"), klasses = Note)
        True

    Otherwise false::

        abjad> componenttools.all_are_components(['foo', 'bar'], klasses = Note)
        False

    Return boolean.
    '''

    if not isinstance(expr, (list, tuple, types.GeneratorType)):
        return False

    if klasses is None:
        klasses = _Component

    for element in expr:
        if not isinstance(element, klasses):
            return False

    return True
