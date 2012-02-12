from abjad.tools import spannertools
from abjad.tools.tietools.TieSpanner import TieSpanner
from abjad.tools.tietools.get_tie_chain import get_tie_chain


def iterate_tie_chains_forward_in_expr(expr):
    r'''Yield left-to-right tie chains in `expr`::

        abjad> notes = notetools.make_notes([0], [(5, 16), (1, 8), (1, 8), (5, 16)])
        abjad> staff = Staff(notes)
        abjad> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 16), staff[1:3])
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
        abjad> print staff.format
        \new Staff {
            c'4 ~
            \times 2/3 {
                c'16
                d'8
            }
            e'8
            f'4 ~
            f'16
        }

    ::

        abjad> for x in tietools.iterate_tie_chains_forward_in_expr(staff):
        ...     x
        ...
        (Note("c'4"), Note("c'16"))
        (Note("d'8"),)
        (Note("e'8"),)
        (Note("f'4"), Note("f'16"))

    Note that one-note tie chains yield the same as other tie chains.

    Note also that nested structures are no problem.

    .. versionchanged:: 2.0
        renamed ``iterate.tie_chains_forward_in()`` to
        ``tietools.iterate_tie_chains_forward_in_expr()``.

    .. versionchanged:: 2.0
        renamed ``iterate.tie_chains_forward_in_expr()`` to
        ``tietools.iterate_tie_chains_forward_in_expr()``.
    '''
    from abjad.tools.leaftools.iterate_leaves_forward_in_expr import iterate_leaves_forward_in_expr

    for leaf in iterate_leaves_forward_in_expr(expr):
        tie_spanners = spannertools.get_spanners_attached_to_component(
            leaf, TieSpanner)
        #if not leaf.tie.spanned or leaf.tie.last:
        if not tie_spanners or tuple(tie_spanners)[0]._is_my_last_leaf(leaf):
            yield get_tie_chain(leaf)
