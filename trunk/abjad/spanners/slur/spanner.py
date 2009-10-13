from abjad.spanners.spanner.positionalhandler import \
   _PositionalGrobHandlerSpanner
from abjad.spanners.slur.format import _SlurSpannerFormatInterface


class Slur(_PositionalGrobHandlerSpanner):

   def __init__(self, music = None):
      _PositionalGrobHandlerSpanner.__init__(self, 'Slur', music)
      self._format = _SlurSpannerFormatInterface(self)
      self.position = None

   ## PRIVATE ATTRIBUTES ##

   _positions = {'neutral':r'\slurNeutral', 'up':r'\slurUp', 
                 'down':r'\slurDown', None:None}
