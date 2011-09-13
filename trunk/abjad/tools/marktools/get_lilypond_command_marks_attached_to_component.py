from abjad.tools.marktools.LilyPondCommandMark import LilyPondCommandMark


def get_lilypond_command_marks_attached_to_component(component, command_name = None):
    r'''.. versionadded:: 2.0

    Get LilyPond command marks attached to `component`::

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

        abjad> marktools.get_lilypond_command_marks_attached_to_component(staff[0])
        (LilyPondCommandMark('slurDotted')(c'8), LilyPondCommandMark('slurUp')(c'8))

    Return tuple of zero or more marks.
    '''

    result = []
    for mark in component._marks_for_which_component_functions_as_start_component:
        if isinstance(mark, LilyPondCommandMark):
            if mark.command_name == command_name or command_name is None:
                result.append(mark)

    result = tuple(result)
    return result
