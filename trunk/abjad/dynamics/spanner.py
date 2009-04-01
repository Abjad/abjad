from abjad.spanner.grobhandler import _GrobHandlerSpanner


class Dynamic(_GrobHandlerSpanner):

   def __init__(self, music, mark):
      _GrobHandlerSpanner.__init__(self, 'DynamicText', music)
      self.mark = mark

   ## PRIVATE ATTRIBUTES ##

   def _right(self, leaf):
      result = [ ]
      if self._isMyFirstLeaf(leaf):
         result.append(r'\%s' % self.mark)
      return result

   ## PUBLIC ATTRIBUTES ##

   @apply
   def mark( ):
      def fget(self):
         return self._mark
      def fset(self, arg):
         assert isinstance(arg, str)
         self._mark = arg
      return property(**locals( ))
