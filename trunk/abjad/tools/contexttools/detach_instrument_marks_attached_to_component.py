def detach_instrument_marks_attached_to_component(component):
    r'''.. versionadded:: 2.1

    Detach instrument marks attached to `component`::

        >>> staff = Staff("c'4 d'4 e'4 f'4")
        >>> instrument_mark = contexttools.InstrumentMark('Violin ', 'Vn. ')
        >>> instrument_mark.attach(staff)
        InstrumentMark(instrument_name='Violin ', short_instrument_name='Vn. ')(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Violin  }
            \set Staff.shortInstrumentName = \markup { Vn.  }
            c'4
            d'4
            e'4
            f'4
        }

    ::

        >>> contexttools.detach_instrument_marks_attached_to_component(staff)
        (InstrumentMark(instrument_name='Violin ', short_instrument_name='Vn. '),)

    ::

        >>> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    Return tuple of zero or more instrument marks.
    '''
    from abjad.tools import contexttools

    marks = []
    for mark in contexttools.get_instrument_marks_attached_to_component(component):
        mark.detach()
        marks.append(mark)

    return tuple(marks)
