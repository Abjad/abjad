from abjad.tools import spannertools


def get_beam_spanner_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Get the only beam spanner attached to `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beam = beamtools.BeamSpanner(staff.leaves)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        >>> beamtools.get_beam_spanner_attached_to_component(staff[0])
        BeamSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> _ is beam
        True

    Return beam spanner.

    Raise missing spanner error when no beam spanner attached to `component`.

    Raise extra spanner error when more than one beam spanner attached to `component`.

    .. versionchanged:: 2.9
        renamed ``spannertools.get_beam_spanner_attached_to_component()`` to
        ``beamtools.get_beam_spanner_attached_to_component()``.
    '''
    from abjad.tools import beamtools

    return spannertools.get_the_only_spanner_attached_to_component(component, beamtools.BeamSpanner)
