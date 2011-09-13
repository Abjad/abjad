from abjad.tools.contexttools.InstrumentMark import InstrumentMark
from abjad.tools.contexttools.get_effective_context_mark import get_effective_context_mark


def get_effective_instrument(component):
    r'''.. versionadded:: 2.0

    Get effective instrument of `component`::

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

        abjad> for note in staff:
        ...     print note, contexttools.get_effective_instrument(note)
        ...
        c'8 InstrumentMark('Flute', 'Fl.')(Staff{4})
        d'8 InstrumentMark('Flute', 'Fl.')(Staff{4})
        e'8 InstrumentMark('Flute', 'Fl.')(Staff{4})
        f'8 InstrumentMark('Flute', 'Fl.')(Staff{4})

    Return instrument mark or none.
    '''

    return get_effective_context_mark(component, InstrumentMark)
