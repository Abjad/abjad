from abjad.tools import componenttools


def move_parentage_children_and_spanners_from_components_to_empty_container(
    components, container):
    r'''Move parentage, children and spanners from donor `components`
    to recipient empty `container`:

    ::

        >>> voice = Voice("{ c'8 [ d'8 } { e'8 f'8 } { g'8 a'8 ] }")

    ::

        >>> f(voice)
        \new Voice {
            {
                c'8 [
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8 ]
            }
        }

    ::

        >>> tuplet = Tuplet(Fraction(3, 4), [])
        >>> containertools.move_parentage_children_and_spanners_from_components_to_empty_container(
        ... voice[:2], tuplet)

    ::

        >>> f(voice)
        \new Voice {
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 3/4 {
                c'8 [
                d'8
                e'8
                f'8
            }
            {
                g'8
                a'8 ]
            }
        }


    Return none.
    '''
    from abjad.tools import containertools
    from abjad.tools.componenttools._give_position_in_parent_from_donor_components_to_container \
        import _give_position_in_parent_from_donor_components_to_container
    from abjad.tools.componenttools._give_children_from_donor_components_to_empty_container \
        import _give_children_from_donor_components_to_empty_container
    from abjad.tools.spannertools._give_spanners_that_dominate_donor_components_to_recipient_components \
        import _give_spanners_that_dominate_donor_components_to_recipient_components

    # check input
    assert componenttools.all_are_contiguous_components_in_same_parent(components)
    assert isinstance(container, containertools.Container), repr(container)
    assert not container, repr(container)

    # move parentage, children and spanners
    _give_children_from_donor_components_to_empty_container(components, container)
    _give_spanners_that_dominate_donor_components_to_recipient_components(components, [container])
    _give_position_in_parent_from_donor_components_to_container(components, container)
