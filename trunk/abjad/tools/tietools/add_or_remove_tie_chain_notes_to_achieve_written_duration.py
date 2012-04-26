from abjad.tools.tietools.TieChain import TieChain
from abjad.tools.tietools.TieSpanner import TieSpanner
from abjad.tools.tietools.get_tie_chain import get_tie_chain
from abjad.tools.tietools.remove_nonfirst_leaves_in_tie_chain import remove_nonfirst_leaves_in_tie_chain


# TODO: Inspect tietools.add_or_remove_tie_chain_notes_to_achieve_written_duration() carefully.
#       Determine whether behavior is correct with LilyPond multipliers.
def add_or_remove_tie_chain_notes_to_achieve_written_duration(tie_chain, new_written_duration):
    r'''Add or remove `tie_chain` notes to achieve `written_duration`::

        abjad> staff = Staff("c'8 [ ]")

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [ ]
        }

    ::

        abjad> tie_chain = tietools.get_tie_chain(staff[0])
        abjad> tietools.add_or_remove_tie_chain_notes_to_achieve_written_duration(tie_chain, Duration(5, 32))
        TieChain((Note("c'8"), Note("c'32")))

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [ ~
            c'32 ]
        }

    Return `tie_chain`.

    .. versionchanged:: 2.0
        renamed ``tietools.duration_change()`` to
        ``tietools.add_or_remove_tie_chain_notes_to_achieve_written_duration()``.
    '''
    from abjad.tools import componenttools
    from abjad.tools import durationtools
    from abjad.tools import notetools
    from abjad.tools import spannertools
    from abjad.tools import tuplettools
    from abjad.tools.spannertools._withdraw_components_from_attached_spanners import \
    _withdraw_components_from_attached_spanners

    assert isinstance(tie_chain, TieChain)
    new_written_duration = durationtools.Duration(new_written_duration)

    if durationtools.is_assignable_rational(new_written_duration):
        tie_chain[0].written_duration = new_written_duration
        remove_nonfirst_leaves_in_tie_chain(tie_chain)
    elif durationtools.is_binary_rational(new_written_duration):
        duration_tokens = notetools.make_notes(0, [new_written_duration])
        for leaf, token in zip(tie_chain, duration_tokens):
            leaf.written_duration = token.written_duration
        if len(tie_chain) == len(duration_tokens):
            pass
        elif len(duration_tokens) < len(tie_chain):
            for leaf in tie_chain[len(duration_tokens):]:
                componenttools.remove_component_subtree_from_score_and_spanners([leaf])
        elif len(tie_chain) < len(duration_tokens):
            spannertools.destroy_spanners_attached_to_component(tie_chain[0], TieSpanner)
            difference = len(duration_tokens) - len(tie_chain)
            extra_leaves = tie_chain[0] * difference
            _withdraw_components_from_attached_spanners(extra_leaves)
            extra_tokens = duration_tokens[len(tie_chain):]
            for leaf, token in zip(extra_leaves, extra_tokens):
                leaf.written_duration = token.written_duration
            if not spannertools.is_component_with_spanner_attached(tie_chain[-1], TieSpanner):
                TieSpanner(list(tie_chain))
            componenttools.extend_in_parent_of_component_and_grow_spanners(tie_chain[-1], extra_leaves)
    else:
        duration_tokens = notetools.make_notes(0, new_written_duration)
        assert isinstance(duration_tokens[0], tuplettools.Tuplet)
        fmtuplet = duration_tokens[0]
        new_chain_written = get_tie_chain(fmtuplet[0]).preprolated_duration
        add_or_remove_tie_chain_notes_to_achieve_written_duration(tie_chain, new_chain_written)
        multiplier = fmtuplet.multiplier
        tuplettools.Tuplet(multiplier, tie_chain.leaves)

    return get_tie_chain(tie_chain[0])
