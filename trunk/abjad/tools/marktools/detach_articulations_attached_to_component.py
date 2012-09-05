def detach_articulations_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Detach articulations attached to `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> slur = spannertools.SlurSpanner(staff.leaves)
        >>> marktools.Articulation('^')(staff[0])
        Articulation('^')(c'8)
        >>> marktools.Articulation('.')(staff[0])
        Articulation('.')(c'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 -\marcato -\staccato (
            d'8
            e'8
            f'8 )
        }

    ::

        >>> marktools.get_articulations_attached_to_component(staff[0])
        (Articulation('^')(c'8), Articulation('.')(c'8))

    ::

        >>> marktools.detach_articulations_attached_to_component(staff[0])
        (Articulation('^'), Articulation('.'))

    ::

        >>> marktools.get_articulations_attached_to_component(staff[0])
        ()

    Return tuple or zero or more articulations detached.
    '''
    from abjad.tools import marktools

    articulations = []
    for articulation in marktools.get_articulations_attached_to_component(component):
        articulation.detach()
        articulations.append(articulation)

    return tuple(articulations)
