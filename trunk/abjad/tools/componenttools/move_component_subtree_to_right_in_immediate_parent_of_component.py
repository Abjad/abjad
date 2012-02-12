from abjad.tools.componenttools.is_orphan_component import is_orphan_component


def move_component_subtree_to_right_in_immediate_parent_of_component(component):
    r'''.. versionadded:: 2.0

    Move `component` subtree to right in immediate parent of `component`::

        abjad> t = Voice("c'8 d'8 e'8 f'8")
        abjad> spannertools.BeamSpanner(t[:2])
        BeamSpanner(c'8, d'8)
        abjad> spannertools.BeamSpanner(t[2:])
        BeamSpanner(e'8, f'8)
        abjad> f(t)
        \new Voice {
            c'8 [
            d'8 ]
            e'8 [
            f'8 ]
        }

    ::

        abjad> componenttools.move_component_subtree_to_right_in_immediate_parent_of_component(t[1])
        abjad> f(t)
        \new Voice {
            c'8 [
            e'8 ]
            d'8 [
            f'8 ]
        }

    Return none.

    .. todo:: add ``n = 1`` keyword to generalize flipped distance.

    .. todo:: make ``componenttools.move_component_subtree_to_right_in_immediate_parent_of_component()`` work when spanners
        attach to children of component:

    ::

        abjad> voice = Voice(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
        abjad> spannertools.BeamSpanner(voice.leaves[:4])
        BeamSpanner(c'8, c'8, c'8, c'8)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(voice)
        abjad> componenttools.move_component_subtree_to_right_in_immediate_parent_of_component(voice[0])
        abjad> f(voice)
        \new Voice {
            \times 2/3 {
                f'8 ]
                g'8
                a'8
            }
            \times 2/3 {
                c'8 [
                d'8
                e'8
            }
        }
        abjad> componenttools.is_well_formed_component(voice)
        False

    Preserve spanners.

    .. versionchanged:: 2.0
        renamed ``componenttools.flip()`` to
        ``componenttools.move_component_subtree_to_right_in_immediate_parent_of_component()``.
    '''

    # swap positions in parent
    if not is_orphan_component(component):
        parent = component._parentage.parent
        parent_index = parent.index(component)
        try:
            next_component = parent[parent_index + 1]
        except IndexError:
            return
        parent._music[parent_index] = next_component
        parent._music[parent_index + 1] = component

    # swap positions in spanners ... tricky!
    component_spanners = {}
    for spanner in component.spanners:
        component_spanners[spanner] = spanner.index(component)
        spanner._sever_component(component)
    next_spanners = {}
    for spanner in next_component.spanners:
        next_spanners[spanner] = spanner.index(next_component)
        spanner._sever_component(next_component)
    for key, value in next_spanners.items():
        key._insert(value, component)
    for key, value in component_spanners.items():
        key._insert(value, next_component)
