from abjad.tools.tietools.TieChain import TieChain
from abjad.tools.tietools.TieSpanner import TieSpanner


def get_tie_chain(component):
    r'''.. versionadded:: 2.0

    Get tie chain from `component`::

        abjad> staff = Staff("c'8 ~ c' d'4")

    ::

        abjad> f(staff)
        \new Staff {
            c'8 ~
            c'8
            d'4
        }

    ::

        abjad> tietools.get_tie_chain(staff[0])
        TieChain((Note("c'8"), Note("c'8")))

    Return tie chain.
    '''
    from abjad.tools import spannertools

    tie_spanners = spannertools.get_spanners_attached_to_component(component, TieSpanner)
    count = len(tie_spanners)

    if count == 0:
        return TieChain(music=component)
    elif count == 1:
        return TieChain(music=tie_spanners.pop().leaves)
    else:
        raise ExtraSpannerError
