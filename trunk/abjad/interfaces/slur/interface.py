from abjad.core.grobhandler import _GrobHandler
from abjad.interfaces.interface.interface import _Interface
from abjad.spanners.slur import Slur
from abjad.spanners.spanner.receptor import _SpannerReceptor


class SlurInterface(_Interface, _GrobHandler, _SpannerReceptor):
   '''Handle LilyPond Slur grob and Abjad Slur spanner.'''

   def __init__(self, client):
      '''Bind to client and LilyPond Slur grob.
         Receive Abjad Slur spanner.'''
      #from abjad.slur import Slur
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Slur')
      _SpannerReceptor.__init__(self, (Slur, ))
