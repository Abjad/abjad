from abjad.tools import componenttools


def is_component_with_stem_tremolo_attached(expr):
    '''.. versionadded:: 2.3

    True when `expr` is component with LilyPond command mark attached::

        >>> note = Note("c'4")
        >>> marktools.StemTremolo(16)(note)
        StemTremolo(16)(c'4)

    ::

        >>> marktools.is_component_with_stem_tremolo_attached(note)
        True

    False otherwise::

        >>> note = Note("c'4")

    ::

        >>> marktools.is_component_with_stem_tremolo_attached(note)
        False

    Return boolean.
    '''
    from abjad.tools import marktools

    if isinstance(expr, componenttools.Component):
        try:
            marktools.get_stem_tremolo_attached_to_component(expr)
            return True
        except (MissingMarkError, ExtraMarkError):
            pass

    return False
