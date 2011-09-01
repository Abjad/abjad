from abjad.tools.marktools.get_stem_tremolo_attached_to_component import get_stem_tremolo_attached_to_component


def is_component_with_stem_tremolo_attached(expr, tremolo_flags = None):
    '''.. versionadded:: 2.3

    True when `expr` is component with LilyPond command mark attached::

        abjad> note = Note("c'4")
        abjad> marktools.StemTremolo(16)(note)
        StemTremolo(16)(c'4)

    ::

        abjad> marktools.is_component_with_stem_tremolo_attached(note)
        True

    False otherwise::

        abjad> note = Note("c'4")

    ::

        abjad> marktools.is_component_with_stem_tremolo_attached(note)
        False

    Return boolean.
    '''
    from abjad.tools.componenttools._Component import _Component

    if isinstance(expr, _Component):
#        for stem_tremolo in get_stem_tremolo_attached_to_component(expr):
#            if stem_tremolo.tremolo_flags == tremolo_flags or tremolo_flags is None:
#                return True
        try:
            get_stem_tremolo_attached_to_component(expr)
            return True
        except (MissingMarkError, ExtraMarkError):
            pass

    return False
