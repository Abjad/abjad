from abjad.octavation.format import _OctavationSpannerFormatInterface
from abjad.spanner.grobhandler import _GrobHandlerSpanner


class Octavation(_GrobHandlerSpanner):

   def __init__(self, music = None, start = 0, stop = 0):
      _GrobHandlerSpanner.__init__(self, 'OttavaBracket', music)
      self._format = _OctavationSpannerFormatInterface(self)
      self.start = start
      self.stop = stop

   ## PUBLIC ATTRIBUTES ##

   @apply
   def start( ):
      def fget(self):
         return self._start
      def fset(self, arg):
         self._start = arg
      return property(**locals( ))

   @apply
   def stop( ):
      def fget(self):
         return self._stop
      def fset(self, arg):
         self._stop = arg
      return property(**locals( ))
