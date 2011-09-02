from abjad.tools.contexttools.InstrumentMark import InstrumentMark
from abjad.tools.contexttools.get_context_marks_attached_to_component import get_context_marks_attached_to_component


def get_instrument_marks_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Get instrument marks attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.InstrumentMark('Flute', 'Fl.')(staff)
        InstrumentMark('Flute', 'Fl.')(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Flute }
            \set Staff.shortInstrumentName = \markup { Fl. }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        abjad> contexttools.get_instrument_marks_attached_to_component(staff)
        (InstrumentMark('Flute', 'Fl.')(Staff{4}),)

    Return tuple of zero or more instrument marks.
    '''

    return get_context_marks_attached_to_component(component, klasses=(InstrumentMark,))
