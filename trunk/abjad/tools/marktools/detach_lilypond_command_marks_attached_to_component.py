from abjad.tools.marktools.get_lilypond_command_marks_attached_to_component import get_lilypond_command_marks_attached_to_component


def detach_lilypond_command_marks_attached_to_component(component, command_name = None):
    r'''.. versionadded:: 2.0

    Detach LilyPond command marks attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> slur = spannertools.SlurSpanner(staff.leaves)
        abjad> marktools.LilyPondCommandMark('slurDotted')(staff[0])
        LilyPondCommandMark('slurDotted')(c'8)
        abjad> marktools.LilyPondCommandMark('slurUp')(staff[0])
        LilyPondCommandMark('slurUp')(c'8)

    ::

        abjad> f(staff)
        \new Staff {
            \slurDotted
            \slurUp
            c'8 (
            d'8
            e'8
            f'8 )
        }

    ::

        abjad> marktools.detach_lilypond_command_marks_attached_to_component(staff[0])
        (LilyPondCommandMark('slurDotted'), LilyPondCommandMark('slurUp'))

    ::

        abjad> f(staff)
        \new Staff {
            c'8 (
            d'8
            e'8
            f'8 )
        }

    Return tuple of zero or more marks detached.
    '''

    marks = []
    for mark in get_lilypond_command_marks_attached_to_component(
        component, command_name = command_name):
        mark.detach()
        marks.append(mark)
    return tuple(marks)
