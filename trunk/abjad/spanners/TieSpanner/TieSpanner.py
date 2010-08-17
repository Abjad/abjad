from abjad.spanners.Spanner import Spanner
from abjad.spanners.TieSpanner._TieSpannerFormatInterface import _TieSpannerFormatInterface


class TieSpanner(Spanner):
   r'''Musical tie between two or more notes, rests or chords.

   ::

      abjad> staff = Staff(notetools.make_repeated_notes(4))
      abjad> TieSpanner(staff[:])
      TieSpanner(c'8, c'8, c'8, c'8)
      abjad> f(staff)
      \new Staff {
         c'8 ~
         c'8 ~
         c'8 ~
         c'8
      }
   '''

   def __init__(self, music = None):
      Spanner.__init__(self, music)
      self._format = _TieSpannerFormatInterface(self)
