from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.tietools.TieSpanner._TieSpannerFormatInterface import _TieSpannerFormatInterface


class TieSpanner(Spanner):
    r'''Abjad tie spanner::

        abjad> staff = Staff(notetools.make_repeated_notes(4))
        abjad> tietools.TieSpanner(staff[:])
        TieSpanner(c'8, c'8, c'8, c'8)
        abjad> f(staff)
        \new Staff {
            c'8 ~
            c'8 ~
            c'8 ~
            c'8
        }

    Return tie spanner.
    '''

    def __init__(self, music = None):
        Spanner.__init__(self, music)
        self._format = _TieSpannerFormatInterface(self)
