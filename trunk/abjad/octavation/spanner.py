from abjad.octavation.format import _OctavationSpannerFormatInterface
from abjad.spanner.grobhandler import _GrobHandlerSpanner
import types


class Octavation(_GrobHandlerSpanner):
   r'''8va or 8vb spanner. Overrides the LilyPond OttavaBracket grob.

   ::

      abjad> t = Staff(construct.scale(4))
      abjad> spanner = Octavation(t[:])
      abjad> spanner.start = 1
      abjad> print t.format
      \new Staff {
         \ottava #1
         c'8
         d'8
         e'8
         f'8
         \ottava #0
      }
   '''

   ## TODO: Remove start and stop from initializer and force set later. ##

   ## TODO: Set start to 1 (and stop to 0) by default. ##

   def __init__(self, music = None, start = 0, stop = 0):
      _GrobHandlerSpanner.__init__(self, 'OttavaBracket', music)
      self._format = _OctavationSpannerFormatInterface(self)
      self.start = start
      self.stop = stop

   ## PUBLIC ATTRIBUTES ##

   @apply
   def start( ):
      def fget(self):
         r'''LilyPond \ottava number before first leaf in spanner. 
         Defaults to ``0``.'''
         return self._start
      def fset(self, arg):
         assert isinstance(arg, (int, types.NoneType))
         self._start = arg
      return property(**locals( ))

   @apply
   def stop( ):
      def fget(self):
         r'''LilyPond \ottava number after last leaf.
         Defaults to ``0``.'''
         return self._stop
      def fset(self, arg):
         assert isinstance(arg, (int, types.NoneType))
         self._stop = arg
      return property(**locals( ))
