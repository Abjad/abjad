from abjad.tools import componenttools
from abjad.tools import spannertools


def is_component_with_beam_spanner_attached(expr):
    r'''.. versionadded:: 2.0

    True when `expr` is component with beam spanner attached.
    Otherwise false.

    ::

        >>> staff = Staff(r"r32 a'32 ( [ gs'32 fs''32 \staccato f''8 ) ]")
        >>> staff.extend(r"r8 e''8 ( ef'2 )")

    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> for note in staff:
        ...     result = beamtools.is_component_with_beam_spanner_attached(note)
        ...     print '{:<8}{}'.format(note, result)
        r32     False
        a'32    True
        gs'32   True
        fs''32  True
        f''8    True
        r8      False
        e''8    False
        ef'2    False

    Return boolean.
    '''
    from abjad.tools import beamtools

    if not isinstance(expr, componenttools.Component):
        return False

    spanner_classes = (beamtools.BeamSpanner, )
    return bool(spannertools.get_spanners_attached_to_component(
        expr, spanner_classes=spanner_classes))
