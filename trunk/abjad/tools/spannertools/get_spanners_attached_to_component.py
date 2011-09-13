def get_spanners_attached_to_component(component, klass = None):
    r'''.. versionadded:: 2.0

    Get all spanners attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> beam = spannertools.BeamSpanner(staff.leaves)
        abjad> first_slur = spannertools.SlurSpanner(staff.leaves[:2])
        abjad> second_slur = spannertools.SlurSpanner(staff.leaves[2:])
        abjad> crescendo = spannertools.CrescendoSpanner(staff.leaves)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [ \< (
            d'8 )
            e'8 (
            f'8 ] \! )
        }

    ::

        abjad> spannertools.get_spanners_attached_to_component(staff.leaves[0]) # doctest: +SKIP
        set([BeamSpanner(c'8, d'8, e'8, f'8), SlurSpanner(c'8, d'8), CrescendoSpanner(c'8, d'8, e'8, f'8)])

    Get spanners of `klass` attached to `component`::

        abjad> klass = spannertools.BeamSpanner
        abjad> spannertools.get_spanners_attached_to_component(staff.leaves[0], klass) # doctest: +SKIP
        set([BeamSpanner(c'8, d'8, e'8, f'8)])

    Get spanners of any `klass` attached to `component`::

        abjad> klasses = (spannertools.BeamSpanner, spannertools.SlurSpanner)
        abjad> spannertools.get_spanners_attached_to_component(staff.leaves[0], klasses) # doctest: +SKIP
        set([BeamSpanner(c'8, d'8, e'8, f'8), SlurSpanner(c'8, d'8)])

    Return unordered set of zero or more spanners.

    .. versionchanged:: 2.0
        renamed ``spannertools.get_all_spanners_attached_to_component()`` to
        ``spannertools.get_spanners_attached_to_component()``.
    '''

    # note: externalization of (old) component spanner aggregator 'spanners' property
    if klass is None:
        #return set(component.spanners.attached)
        #return set(component.spanners._spanners)
        return component.spanners
    else:
        #return set([x for x in component.spanners.attached if isinstance(x, klass)])
        #return set([x for x in component.spanners._spanners if isinstance(x, klass)])
        return set([x for x in component.spanners if isinstance(x, klass)])
