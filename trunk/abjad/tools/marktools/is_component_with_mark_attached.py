from abjad.tools.marktools.get_marks_attached_to_component import get_marks_attached_to_component


def is_component_with_mark_attached(expr):
    '''.. versionadded:: 2.3

    True when `expr` is component with mark attached::

        abjad> note = Note("c'4")
        abjad> marktools.Mark()(note)
        Mark()(c'4)

    ::

        abjad> marktools.is_component_with_mark_attached(note)
        True

    False otherwise::

        abjad> note = Note("c'4")

    ::

        abjad> marktools.is_component_with_mark_attached(note)
        False

    Return boolean.
    '''
    from abjad.tools.componenttools._Component import _Component

    if isinstance(expr, _Component):
        return bool(get_marks_attached_to_component(expr))
