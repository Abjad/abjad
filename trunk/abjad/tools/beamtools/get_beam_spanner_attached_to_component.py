from abjad.tools import spannertools


def get_beam_spanner_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Get the only beam spanner attached to `component`:

    ::

        >>> staff = Staff(r"r32 a'32 ( [ gs'32 fs''32 \staccato f''8 ) ]")
        >>> staff.extend(r"r8 e''8 ( ef'2 )")

    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> note = staff[1]
        >>> beamtools.get_beam_spanner_attached_to_component(note)
        BeamSpanner(a'32, gs'32, fs''32, f''8)

    Return beam spanner.

    Raise missing spanner error when no beam spanner attached to `component`.

    Raise extra spanner error when more than one beam spanner 
    attached to `component`.
    '''
    from abjad.tools import beamtools

    spanner_classes = (beamtools.BeamSpanner, )
    return spannertools.get_the_only_spanner_attached_to_component(
        component, spanner_classes=spanner_classes)
