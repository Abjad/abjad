def get_effective_instrument(component):
    r'''.. versionadded:: 2.0

    Get effective instrument of `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contexttools.InstrumentMark('Flute', 'Fl.')(staff)
        InstrumentMark(instrument_name='Flute', short_instrument_name='Fl.')(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Flute }
            \set Staff.shortInstrumentName = \markup { Fl. }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> for note in staff:
        ...     print note, contexttools.get_effective_instrument(note)
        ...
        c'8 InstrumentMark(instrument_name='Flute', short_instrument_name='Fl.')(Staff{4})
        d'8 InstrumentMark(instrument_name='Flute', short_instrument_name='Fl.')(Staff{4})
        e'8 InstrumentMark(instrument_name='Flute', short_instrument_name='Fl.')(Staff{4})
        f'8 InstrumentMark(instrument_name='Flute', short_instrument_name='Fl.')(Staff{4})

    Return instrument mark or none.
    '''
    from abjad.tools import contexttools

    return contexttools.get_effective_context_mark(component, contexttools.InstrumentMark)
