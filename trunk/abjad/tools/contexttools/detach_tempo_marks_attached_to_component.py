from abjad.tools.contexttools.get_tempo_marks_attached_to_component import get_tempo_marks_attached_to_component


def detach_tempo_marks_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Detach tempo marks attached to `component`::

        abjad> score = Score([])
        abjad> staff = Staff("c'4 d'4 e'4 f'4")
        abjad> score.append(staff)

    ::

        abjad> tempo_mark = contexttools.TempoMark(Duration(1, 8), 52)
        abjad> tempo_mark.attach(staff)
        TempoMark(8, 52)(Staff{4})

    ::

        abjad> f(score)
        \new Score <<
            \tempo 8=52
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }
        >>

    ::

        abjad> contexttools.detach_tempo_marks_attached_to_component(staff)
        (TempoMark(8, 52),)

    ::

        abjad> f(score)
        \new Score <<
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }
        >>

    Return tuple of zero or more tempo marks.
    '''

    marks = []
    for mark in get_tempo_marks_attached_to_component(component):
        mark.detach()
        marks.append(mark)
    return tuple(marks)
