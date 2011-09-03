from abjad.tools.tuplettools.Tuplet import Tuplet
from abjad.tools import componenttools


def move_prolation_of_tuplet_to_contents_of_tuplet_and_remove_tuplet(tuplet):
    r'''Scale ``tuplet`` contents and then bequeath in-score \
    position of ``tuplet`` to contents.

    Return orphaned ``tuplet`` emptied of all contents. ::

        abjad> t = Staff(tuplettools.FixedDurationTuplet(Duration(3, 8), "c'8 d'8") * 2)
        abjad> spannertools.BeamSpanner(t.leaves)
        BeamSpanner(c'8, d'8, c'8, d'8)
        abjad> print t.format
        \new Staff {
            \fraction \times 3/2 {
                c'8 [
                d'8
            }
            \fraction \times 3/2 {
                c'8
                d'8 ]
            }
        }

    ::

        abjad> tuplettools.move_prolation_of_tuplet_to_contents_of_tuplet_and_remove_tuplet(t[0])
        FixedDurationTuplet(3/8, [])
        abjad> print t.format
        \new Staff {
            c'8. [
            d'8.
            \fraction \times 3/2 {
                c'8
                d'8 ]
            }
        }

    .. versionchanged:: 2.0
        renamed ``tuplettools.subsume()`` to
        ``tuplettools.move_prolation_of_tuplet_to_contents_of_tuplet_and_remove_tuplet()``.
    '''

    assert isinstance(tuplet, Tuplet)
    from abjad.tools import containertools

    containertools.scale_contents_of_container(tuplet, tuplet.multiplier)
    componenttools.move_parentage_and_spanners_from_components_to_components([tuplet], tuplet[:])

    return tuplet
