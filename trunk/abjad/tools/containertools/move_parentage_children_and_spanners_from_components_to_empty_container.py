from abjad.tools import componenttools


def move_parentage_children_and_spanners_from_components_to_empty_container(components, container):
    r'''Move parentage, children and spanners from donor `components` 
    to recipient empty `container`::

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
            \fraction \times 3/4 {
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
    from abjad.tools.componenttools._give_donor_components_position_in_parent_to_recipient_components import \
        _give_donor_components_position_in_parent_to_recipient_components
    from abjad.tools.componenttools._give_music_from_donor_components_to_recipient_components import \
        _give_music_from_donor_components_to_recipient_components
    from abjad.tools.spannertools._give_spanners_that_dominate_donor_components_to_recipient_components import \
        _give_spanners_that_dominate_donor_components_to_recipient_components

    assert componenttools.all_are_contiguous_components_in_same_parent(components)

    if not isinstance(container, containertools.Container):
        raise TypeError

    if not len(container) == 0:
        raise MusicContentsError

    _give_music_from_donor_components_to_recipient_components(components, container)
    _give_spanners_that_dominate_donor_components_to_recipient_components(components, [container])
    _give_donor_components_position_in_parent_to_recipient_components(components, [container])
