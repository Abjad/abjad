from abjad.spanners.Spanner._GrobHandlerSpanner import _GrobHandlerSpanner
from abjad.spanners.TieSpanner._TieSpannerFormatInterface import _TieSpannerFormatInterface


class TieSpanner(_GrobHandlerSpanner):
   r'''Musical tie between two or more notes, rests or chords.

   ::

      abjad> staff = Staff(notetools.make_repeated_notes(4))
      abjad> Tie(staff[:])
      Tie(c'8, c'8, c'8, c'8)
      abjad> f(staff)
      \new Staff {
         c'8 ~
         c'8 ~
         c'8 ~
         c'8
      }
   '''

   def __init__(self, music = None):
      _GrobHandlerSpanner.__init__(self, 'Tie', music)
      self._format = _TieSpannerFormatInterface(self)
