from abjad.tools.containertools.Container import Container
from abjad.tools.componenttools._give_donor_components_position_in_parent_to_recipient_components import _give_donor_components_position_in_parent_to_recipient_components
from abjad.tools.componenttools._give_music_from_donor_components_to_recipient_components import _give_music_from_donor_components_to_recipient_components
from abjad.tools.spannertools._give_spanners_that_dominate_donor_components_to_recipient_components import _give_spanners_that_dominate_donor_components_to_recipient_components


def move_parentage_children_and_spanners_from_components_to_empty_container(donors, recipient):
    r'''Move parentage, children and spanners from `components` to empty `container`::

        abjad> voice = Voice(Container("c'8 c'8") * 3)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(voice)
        abjad> spannertools.BeamSpanner(voice.leaves)
        BeamSpanner(c'8, d'8, e'8, f'8, g'8, a'8)

    ::

        abjad> f(voice)
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

        abjad> tuplet = Tuplet(Fraction(3, 4), [])
        abjad> containertools.move_parentage_children_and_spanners_from_components_to_empty_container(voice[:2], tuplet)

    ::

        abjad> f(voice)
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

    .. versionchanged:: 2.0
        renamed ``scoretools.donate()`` to
        ``containertools.move_parentage_children_and_spanners_from_components_to_empty_container()``.
    '''
    from abjad.tools import componenttools

    assert componenttools.all_are_contiguous_components_in_same_parent(donors)

    if not isinstance(recipient, Container):
        raise TypeError

    if not len(recipient) == 0:
        raise MusicContentsError

    _give_music_from_donor_components_to_recipient_components(donors, recipient)
    _give_spanners_that_dominate_donor_components_to_recipient_components(donors, [recipient])
    _give_donor_components_position_in_parent_to_recipient_components(donors, [recipient])
