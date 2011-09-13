from abjad.exceptions import ExtraSpannerError
from abjad.tools import spannertools
from abjad.tools.tietools.TieSpanner import TieSpanner


def get_tie_chain(component):
    '''.. versionadded:: 2.0

    Get tie chain from `component`.
    '''

    tie_spanners = spannertools.get_spanners_attached_to_component(component, TieSpanner)
    count = len(tie_spanners)

    if count == 0:
        return (component, )
    elif count == 1:
        return tuple(tie_spanners.pop().leaves)
    else:
        raise ExtraSpannerError
