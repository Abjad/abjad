from abjad.exceptions import ExtraMarkError
from abjad.exceptions import MissingMarkError
from abjad.tools.contexttools.InstrumentMark import InstrumentMark


def get_instrument_mark_attached_to_component(component):
    r'''.. versionadded:: 2.1

    Get instrument mark attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> violin = contexttools.InstrumentMark('Violin ', 'Vn. ')
        abjad> violin.attach_mark(staff)

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

    result = [ ]
    for mark in component._marks_for_which_component_functions_as_start_component:
        if isinstance(mark, InstrumentMark):
            result.append(mark)

    if len(result) == 0:
        raise MissingMarkError
    if 1 < len(result):
        raise ExtraMarkError

    result = result[0]

    return result
