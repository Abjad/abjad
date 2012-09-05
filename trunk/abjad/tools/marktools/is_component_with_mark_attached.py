from abjad.tools import componenttools


def is_component_with_mark_attached(expr):
    '''.. versionadded:: 2.3

    True when `expr` is component with mark attached::

        >>> note = Note("c'4")
        >>> marktools.Mark()(note)
        Mark()(c'4)

    ::

        >>> marktools.is_component_with_mark_attached(note)
        True

    False otherwise::

        >>> note = Note("c'4")

    ::

        >>> marktools.is_component_with_mark_attached(note)
        False

    Return boolean.
    '''
    from abjad.tools import marktools

    if isinstance(expr, componenttools.Component):
        return bool(marktools.get_marks_attached_to_component(expr))
