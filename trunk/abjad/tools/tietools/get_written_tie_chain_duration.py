from abjad.exceptions import MissingSpannerError
from abjad.tools import spannertools
from abjad.tools.tietools.TieSpanner import TieSpanner
from abjad.tools.tietools.is_tie_chain import is_tie_chain


def get_written_tie_chain_duration(tie_chain):
    '''Return sum of written duration of all leaves in chain.
    '''

    assert is_tie_chain(tie_chain)

    try:
        tie_spanner = spannertools.get_the_only_spanner_attached_to_component(tie_chain[0], TieSpanner)
        return tie_spanner.written_duration
    except MissingSpannerError:
        return tie_chain[0].written_duration
