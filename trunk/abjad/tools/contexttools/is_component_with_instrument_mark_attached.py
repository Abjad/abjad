from abjad.tools.contexttools.InstrumentMark import InstrumentMark
from abjad.tools.contexttools.is_component_with_context_mark_attached import is_component_with_context_mark_attached


def is_component_with_instrument_mark_attached(expr):
    r'''.. versionadded:: 2.3

    True when `expr` is a component with instrument mark attached:: 

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> violin = contexttools.InstrumentMark('Violin ', 'Vn. ')
        abjad> violin.attach(staff)
        InstrumentMark('Violin ', 'Vn. ')(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Violin  }
            \set Staff.shortInstrumentName = \markup { Vn.  }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        abjad> contexttools.is_component_with_instrument_mark_attached(staff)
        True

    Otherwise false::
    
        abjad> contexttools.is_component_with_instrument_mark_attached(staff[0])
        False

    Return boolean.
    '''
    
    return is_component_with_context_mark_attached(expr, klasses=(InstrumentMark,))
