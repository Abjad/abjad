from abjad.tools.marktools.get_noncontext_marks_attached_to_component import get_noncontext_marks_attached_to_component


def is_component_with_noncontext_mark_attached(expr):
    '''.. versionadded:: 2.3

    True when `expr` is component with noncontext mark attached::

        abjad> note = Note("c'4")
        abjad> marktools.Articulation('staccato')(note)
        Articulation('staccato')(c'4)

    ::

        abjad> marktools.is_component_with_noncontext_mark_attached(note)
        True

    False otherwise::

        abjad> note = Note("c'4")

    ::

        abjad> marktools.is_component_with_noncontext_mark_attached(note)
        False
     
    Return boolean.
    '''
    from abjad.tools.componenttools._Component import _Component

    if isinstance(expr, _Component):
        for noncontext_mark in get_noncontext_marks_attached_to_component(expr):
            return True

    return False
