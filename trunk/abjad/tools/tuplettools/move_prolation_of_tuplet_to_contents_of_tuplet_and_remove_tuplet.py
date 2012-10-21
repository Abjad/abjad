from abjad.tools import componenttools
from abjad.tools import containertools


def move_prolation_of_tuplet_to_contents_of_tuplet_and_remove_tuplet(tuplet):
    r'''Move prolation of `tuplet` to contents of `tuplet` and remove `tuplet`::

        >>> t = Staff(r"\times 3/2 { c'8 [ d'8 } \times 3/2 { c'8 d'8 ] }")

    ::

        >>> f(t)
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

        >>> tuplettools.move_prolation_of_tuplet_to_contents_of_tuplet_and_remove_tuplet(t[0])
        Tuplet(3/2, [])

    ::

        >>> f(t)
        \new Staff {
            c'8. [
            d'8.
            \fraction \times 3/2 {
                c'8
                d'8 ]
            }
        }

    Return `tuplet`.
    '''
    from abjad.tools import tuplettools

    assert isinstance(tuplet, tuplettools.Tuplet)

    containertools.scale_contents_of_container(tuplet, tuplet.multiplier)
    componenttools.move_parentage_and_spanners_from_components_to_components([tuplet], tuplet[:])

    return tuplet
