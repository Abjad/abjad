from abjad.exceptions import MissingSpannerError
from abjad.tools import spannertools
from abjad.tools.tietools.TieSpanner import TieSpanner
from abjad.tools.tietools.is_tie_chain import is_tie_chain


def get_preprolated_tie_chain_duration(tie_chain):
    '''Get sum of preprolated duration of all leaves in `tie_chain`.

    .. todo:: write ``tietools.get_preprolated_tie_chain_duration()`` tests.

    .. versionchanged:: 2.0
        renamed ``tietools.get_duration_preprolated()`` to
        ``tietools.get_preprolated_tie_chain_duration()``.
    '''

    assert is_tie_chain(tie_chain)

    try:
        #return tie_chain[0].tie.spanner.preprolated_duration
        tie_spanner = spannertools.get_the_only_spanner_attached_to_component(
            tie_chain[0], TieSpanner)
        return tie_spanner.preprolated_duration
    except MissingSpannerError:
        return tie_chain[0].preprolated_duration
