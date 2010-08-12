from abjad.spanners.Hairpin._HairpinSpannerFormatInterface import _HairpinSpannerFormatInterface
from abjad.spanners.Spanner._GrobHandlerSpanner import _GrobHandlerSpanner


class Hairpin(_GrobHandlerSpanner):

   def __init__(self, music, descriptor, trim = False):
      _GrobHandlerSpanner.__init__(self, 'DynamicLineSpanner', music)
      self._format = _HairpinSpannerFormatInterface(self)
      start, shape, stop = self._parse_descriptor(descriptor)
      self.shape = shape
      self.start = start
      self.stop = stop
      self.trim = trim
   
   ## PRIVATE METHODS ##

   def _parse_descriptor(self, descriptor):
      '''Example descriptors:
         '<'
         'p <'
         'p < f'
      '''
      assert isinstance(descriptor, str)
      parts = descriptor.split( )
      num_parts = len(parts)
      start, shape, stop = None, None, None
      if parts[0] in ('<', '>'):
         assert 1 <= num_parts <= 2
         if num_parts == 1:
            shape = parts[0]
         else:
            shape = parts[0]
            stop = parts[1]
      else:
         assert 2 <= num_parts <= 3
         if num_parts == 2:
            start = parts[0]
            shape = parts[1]
         else:
            start = parts[0]
            shape = parts[1]
            stop = parts[2]
      assert shape in ('<', '>')
      return start, shape, stop

   ## PUBLIC ATTRIBUTES ##

   @apply
   def shape( ):
      def fget(self):
         return self._shape
      def fset(self, arg):
         assert arg in ('<', '>')
         self._shape = arg
      return property(**locals( ))

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

   @apply
   def trim( ):
      def fget(self):
         return self._trim
      def fset(self, arg):
         self._trim = arg
      return property(**locals( ))
