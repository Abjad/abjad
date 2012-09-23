import copy


def attach_lilypond_command_marks_to_components_in_expr(expr, lilypond_command_marks):
    r'''.. versionadded:: 2.3

    Attach `lilypond_command_marks` to components in `expr`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> lilypond_command_mark = marktools.LilyPondCommandMark('stemUp')
        >>> marktools.attach_lilypond_command_marks_to_components_in_expr(
        ...     staff.leaves, [lilypond_command_mark])

    ::

        >>> f(staff)
        \new Staff {
            \stemUp
            c'8
            \stemUp
            d'8
            \stemUp
            e'8
            \stemUp
            f'8
        }

    Return none.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import marktools

    for component in iterationtools.iterate_components_in_expr(expr):
        for lilypond_command_mark in lilypond_command_marks:
            marktools.LilyPondCommandMark(lilypond_command_mark)(component)
