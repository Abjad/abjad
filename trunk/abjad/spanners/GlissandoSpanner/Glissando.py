from abjad.spanners.Glissando._GlissandoSpannerFormatInterface import \
   _GlissandoSpannerFormatInterface
from abjad.spanners.Spanner._GrobHandlerSpanner import _GrobHandlerSpanner


class Glissando(_GrobHandlerSpanner):
   '''Model glissando covering two or more notes.
      Handle LilyPond ``Glissando`` grob.'''

   def __init__(self, music = None):
      '''Handle LilyPond ``Glissando`` grob.'''
      _GrobHandlerSpanner.__init__(self, 'Glissando', music)
      self._format = _GlissandoSpannerFormatInterface(self)
