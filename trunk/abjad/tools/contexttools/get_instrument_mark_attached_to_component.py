def get_instrument_mark_attached_to_component(component):
    r'''.. versionadded:: 2.1

    Get instrument mark attached to `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> violin = contexttools.InstrumentMark('Violin ', 'Vn. ')
        >>> violin.attach(staff)
        InstrumentMark(instrument_name='Violin ', short_instrument_name='Vn. ')(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Violin  }
            \set Staff.shortInstrumentName = \markup { Vn.  }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> contexttools.get_instrument_mark_attached_to_component(staff)
        InstrumentMark(instrument_name='Violin ', short_instrument_name='Vn. ')(Staff{4})

    Return instrument mark.

    Raise missing mark error when no instrument mark attaches to `component`.
    '''
    from abjad.tools import contexttools
    
    return contexttools.get_context_mark_attached_to_component(component, klasses=(contexttools.InstrumentMark,))
