from abjad.tools.contexttools.get_instrument_marks_attached_to_component import get_instrument_marks_attached_to_component


def detach_instrument_marks_attached_to_component(component):
    r'''.. versionadded:: 2.1

    Detach instrument marks attached to `component`::

        abjad> staff = Staff("c'4 d'4 e'4 f'4")
        abjad> instrument_mark = contexttools.InstrumentMark('Violin ', 'Vn. ')
        abjad> instrument_mark.attach(staff)
        InstrumentMark('Violin ', 'Vn. ')(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Violin  }
            \set Staff.shortInstrumentName = \markup { Vn.  }
            c'4
            d'4
            e'4
            f'4
        }

    ::

        abjad> contexttools.detach_instrument_marks_attached_to_component(staff)
        (InstrumentMark('Violin ', 'Vn. '),)

    ::

        abjad> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    Return tuple of zero or more instrument marks.
    '''

    marks = []
    for mark in get_instrument_marks_attached_to_component(component):
        mark.detach()
        marks.append(mark)
    return tuple(marks)
