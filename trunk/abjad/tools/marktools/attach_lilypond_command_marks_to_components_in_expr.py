from abjad.tools.marktools.LilyPondCommandMark import LilyPondCommandMark
import copy


def attach_lilypond_command_marks_to_components_in_expr(expr, lilypond_command_marks):
    r'''.. versionadded:: 2.3

    Attach `lilypond_command_marks` to components in `expr`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> lilypond_command_mark = marktools.LilyPondCommandMark('stemUp')
        abjad> marktools.attach_lilypond_command_marks_to_components_in_expr(staff.leaves, [lilypond_command_mark])

    ::

        abjad> f(staff)
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
    from abjad.tools import componenttools

    for component in componenttools.iterate_components_forward_in_expr(expr):
        for lilypond_command_mark in lilypond_command_marks:
            LilyPondCommandMark(lilypond_command_mark)(component)
