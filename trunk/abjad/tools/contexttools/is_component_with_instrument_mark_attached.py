def is_component_with_instrument_mark_attached(expr):
    r'''.. versionadded:: 2.3

    True when `expr` is a component with instrument mark attached:: 

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

        >>> contexttools.is_component_with_instrument_mark_attached(staff)
        True

    Otherwise false::
    
        >>> contexttools.is_component_with_instrument_mark_attached(staff[0])
        False

    Return boolean.
    '''
    from abjad.tools import contexttools
    
    return contexttools.is_component_with_context_mark_attached(expr, klasses=(contexttools.InstrumentMark,))
