from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import spannertools
from abjad.tools.spannertools._withdraw_components_from_attached_spanners import _withdraw_components_from_attached_spanners
from abjad.tools.tietools.TieSpanner import TieSpanner
from abjad.tools.tietools.get_leaves_in_tie_chain import get_leaves_in_tie_chain
from abjad.tools.tietools.get_preprolated_tie_chain_duration import get_preprolated_tie_chain_duration
from abjad.tools.tietools.get_tie_chain import get_tie_chain
from abjad.tools.tietools.is_tie_chain import is_tie_chain
from abjad.tools.tietools.remove_all_leaves_in_tie_chain_except_first import remove_all_leaves_in_tie_chain_except_first
from abjad.tools import durationtools


# TODO: Inspect tietools.add_or_remove_tie_chain_notes_to_achieve_written_duration() carefully. #
#       Determine whether behavior is correct with LilyPond multipliers. #

def add_or_remove_tie_chain_notes_to_achieve_written_duration(tie_chain, new_written_duration):
    '''Change the written duration of tie chain,
    adding and subtracting notes as necessary.

    Return newly modified tie chain.

    .. versionchanged:: 2.0
        renamed ``tietools.duration_change()`` to
        ``tietools.add_or_remove_tie_chain_notes_to_achieve_written_duration()``.
    '''
    from abjad.tools.tuplettools.Tuplet import Tuplet
    from abjad.tools import notetools

    assert is_tie_chain(tie_chain)
    #assert isinstance(new_written_duration, Duration)
    new_written_duration = durationtools.Duration(new_written_duration)

    if durationtools.is_assignable_rational(new_written_duration):
        tie_chain[0].written_duration = new_written_duration
        remove_all_leaves_in_tie_chain_except_first(tie_chain)
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
            #tie_chain[0].tie.unspan()
            spannertools.destroy_all_spanners_attached_to_component(tie_chain[0], TieSpanner)
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
        assert isinstance(duration_tokens[0], Tuplet)
        fmtuplet = duration_tokens[0]
        new_chain_written = get_preprolated_tie_chain_duration(
            get_tie_chain(fmtuplet[0]))
        add_or_remove_tie_chain_notes_to_achieve_written_duration(tie_chain, new_chain_written)
        multiplier = fmtuplet.multiplier
        Tuplet(multiplier, get_leaves_in_tie_chain(tie_chain))

    return get_tie_chain(tie_chain[0])
