from abjad.tools.contexttools.InstrumentMark import InstrumentMark
from abjad.tools.contexttools.get_context_mark_attached_to_component import get_context_mark_attached_to_component


def get_instrument_mark_attached_to_component(component):
    r'''.. versionadded:: 2.1

    Get instrument mark attached to `component`::

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

        abjad> contexttools.get_instrument_mark_attached_to_component(staff)
        InstrumentMark('Violin ', 'Vn. ')(Staff{4})

    Return instrument mark.

    Raise missing mark error when no instrument mark attaches to `component`.
    '''
    
    return get_context_mark_attached_to_component(component, klasses=(InstrumentMark,))
