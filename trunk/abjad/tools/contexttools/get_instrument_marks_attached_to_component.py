def get_instrument_marks_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Get instrument marks attached to `component`::

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

        >>> contexttools.get_instrument_marks_attached_to_component(staff)
        (InstrumentMark(instrument_name='Flute', short_instrument_name='Fl.')(Staff{4}),)

    Return tuple of zero or more instrument marks.
    '''
    from abjad.tools import contexttools

    return contexttools.get_context_marks_attached_to_component(component, klasses=(contexttools.InstrumentMark,))
