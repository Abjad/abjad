from abjad.tools.containertools.Container import Container
from abjad.tools.tuplettools.Tuplet import Tuplet
from abjad.exceptions import TupletFuseError
from abjad.tools.componenttools.component_to_score_root import component_to_score_root
from abjad.tools.tuplettools.FixedDurationTuplet import FixedDurationTuplet
from abjad.tools import durationtools


def fuse_tuplets(tuplets):
    r'''Fuse parent-contiguous `tuplets`::

        abjad> t1 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
        abjad> spannertools.BeamSpanner(t1[:])
        BeamSpanner(c'8, d'8, e'8)
        abjad> t2 = tuplettools.FixedDurationTuplet(Duration(2, 16), "c'16 d'16 e'16")
        abjad> spannertools.SlurSpanner(t2[:])
        SlurSpanner(c'16, d'16, e'16)
        abjad> staff = Staff([t1, t2])
        abjad> f(staff)
        \new Staff {
            \times 2/3 {
                c'8 [
                d'8
                e'8 ]
            }
            \times 2/3 {
                c'16 (
                d'16
                e'16 )
            }
        }

    ::

        abjad> tuplettools.fuse_tuplets(staff[:])
        FixedDurationTuplet(3/8, [c'8, d'8, e'8, c'16, d'16, e'16])

    ::

        abjad> f(staff)
        \new Staff {
            \times 2/3 {
                c'8 [
                d'8
                e'8 ]
                c'16 (
                d'16
                e'16 )
            }
        }

    Return new tuplet.

    Fuse zero or more parent-contiguous `tuplets`.

    Allow in-score `tuplets`.

    Allow outside-of-score `tuplets`.

    All `tuplets` must carry the same multiplier.

    All `tuplets` must be of the same type.

    .. versionchanged:: 2.0
        renamed ``fuse.tuplets_by_reference()`` to
        ``tuplettools.fuse_tuplets()``.
    '''

    from abjad.tools import componenttools
    from abjad.tools import containertools
    from abjad.tools import scoretools

    assert componenttools.all_are_contiguous_components_in_same_parent(tuplets, klasses = (Tuplet))

    if len(tuplets) == 0:
        return None

    first = tuplets[0]
    first_multiplier = first.multiplier
    first_type = type(first)
    for tuplet in tuplets[1:]:
        if tuplet.multiplier != first_multiplier:
            raise TupletFuseError('tuplets must carry same multiplier.')
        if type(tuplet) != first_type:
            raise TupletFuseError('tuplets must be same type.')

    if isinstance(first, FixedDurationTuplet):
        total_contents_duration = sum([x.contents_duration for x in tuplets])
        new_target_duration = first_multiplier * total_contents_duration
        new_tuplet = FixedDurationTuplet(new_target_duration, [])
    elif isinstance(first, Tuplet):
        new_tuplet = Tuplet(first_multiplier, [])
    else:
        raise TypeError('unknown tuplet type.')

    wrapped = False
    if component_to_score_root(tuplets[0]) is not component_to_score_root(tuplets[-1]):
        dummy_container = Container(tuplets)
        wrapped = True
    containertools.move_parentage_children_and_spanners_from_components_to_empty_container(
        tuplets, new_tuplet)

    if wrapped:
        containertools.delete_contents_of_container(dummy_container)

    return new_tuplet
