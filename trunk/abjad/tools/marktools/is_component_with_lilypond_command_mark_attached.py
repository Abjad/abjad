from abjad.tools import componenttools


def is_component_with_lilypond_command_mark_attached(expr, command_name=None):
    '''.. versionadded:: 2.0

    True when `expr` is component with LilyPond command mark attached::

        >>> note = Note("c'4")
        >>> marktools.LilyPondCommandMark('stemUp')(note)
        LilyPondCommandMark('stemUp')(c'4)

    ::

        >>> marktools.is_component_with_lilypond_command_mark_attached(note)
        True

    False otherwise::

        >>> note = Note("c'4")

    ::

        >>> marktools.is_component_with_lilypond_command_mark_attached(note)
        False

    Return boolean.
    '''
    from abjad.tools import marktools

    if isinstance(expr, componenttools.Component):
        for mark in marktools.get_lilypond_command_marks_attached_to_component(expr):
            if mark.command_name == command_name or command_name is None:
                return True

    return False
