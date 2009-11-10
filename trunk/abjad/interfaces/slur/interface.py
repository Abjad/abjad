from abjad.core.grobhandler import _GrobHandler
from abjad.interfaces.interface.interface import _Interface
from abjad.interfaces.spanner_receptor.receptor import _SpannerReceptor
from abjad.spanners import Slur


class SlurInterface(_Interface, _GrobHandler, _SpannerReceptor):
   '''Handle LilyPond Slur grob and Abjad Slur spanner.'''

   def __init__(self, client):
      '''Bind to client and LilyPond Slur grob.
         Receive Abjad Slur spanner.'''
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Slur')
      _SpannerReceptor.__init__(self, (Slur, ))
