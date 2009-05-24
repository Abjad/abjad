from abjad.glissando.format import _GlissandoSpannerFormatInterface
from abjad.spanner.grobhandler import _GrobHandlerSpanner


class Glissando(_GrobHandlerSpanner):
   '''Model glissando covering two or more notes.
      Handle *LilyPond* ``Glissando`` grob.'''

   def __init__(self, music = None):
      '''Handle *LilyPond* ``Glissando`` grob.'''
      _GrobHandlerSpanner.__init__(self, 'Glissando', music)
      self._format = _GlissandoSpannerFormatInterface(self)
