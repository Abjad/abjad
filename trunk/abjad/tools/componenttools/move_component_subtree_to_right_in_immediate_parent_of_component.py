def move_component_subtree_to_right_in_immediate_parent_of_component(component):
    r'''.. versionadded:: 2.0

    Move `component` subtree to right in immediate parent of `component`::

        >>> voice = Voice("c'8 [ d'8 ] e'8 [ f'8 ]")

    ::

        >>> f(voice)
        \new Voice {
            c'8 [
            d'8 ]
            e'8 [
            f'8 ]
        }

    ::

        >>> componenttools.move_component_subtree_to_right_in_immediate_parent_of_component(
        ... voice[1])

    ::

        >>> f(voice)
        \new Voice {
            c'8 [
            e'8 ]
            d'8 [
            f'8 ]
        }

    Return none.

    .. todo:: add ``n = 1`` keyword to generalize flipped distance.

    .. todo:: make 
        ``componenttools.move_component_subtree_to_right_in_immediate_parent_of_component()`` 
        work when spanners attach to children of component:

    ::

        >>> voice = Voice(r"\times 2/3 { c'8 [ d'8 e'8 } \times 2/3 { f'8 ] g'8 a'8 }")

    ::

        >>> componenttools.move_component_subtree_to_right_in_immediate_parent_of_component(
        ... voice[0])

    ::

        >>> f(voice)
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

    ::

        >>> componenttools.is_well_formed_component(voice)
        False

    Preserve spanners.

    .. versionchanged:: 2.0
        renamed ``componenttools.flip()`` to
        ``componenttools.move_component_subtree_to_right_in_immediate_parent_of_component()``.
    '''
    from abjad.tools import componenttools

    # swap positions in parent
    if not componenttools.is_orphan_component(component):
        parent = component._parent
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
