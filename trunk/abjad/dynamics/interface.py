from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.spanner.receptor import _SpannerReceptor


## TODO: Dynamics by spanner only? ##
## TODO: Multistage dynamic spanner? ##

class _DynamicsInterface(_Interface, _GrobHandler, _SpannerReceptor):
   
   def __init__(self, client):
      from abjad.dynamics.spanner import Dynamic
      from abjad.hairpin.hairpin import Hairpin
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'DynamicText')
      _SpannerReceptor.__init__(self, (Dynamic, Hairpin))
      self._mark = None

   ## PRIVATE ATTRIBUTES ##

   @property
   def _right(self):
      result = [ ]
      if self.mark:
         result.append(r'\%s' % self.mark)
      return result

   @property
   def _summary(self):
      result = [ ]
      if self.mark:
         result.append(self.mark)
      if self.spanner:
         result.append(self.spanner)
      if result:
         return ', '.join([str(x) for x in result])
      else:
         return ' '

   ## PUBLIC ATTRIBUTES ##

   @property
   def effective(self):
      from abjad.dynamics.spanner import Dynamic
      from abjad.hairpin.hairpin import Hairpin
      if self.mark:
         return self.mark
      if self.spanned:
         spanner = self.spanner
         if isinstance(spanner, Dynamic):
            return spanner.mark
         elif isinstance(spanner, Hairpin):
            return spanner.shape
         else:
            raise Exception
      prev = self._client.prev
      if prev is not None:
         return prev.dynamics.effective
      return None

   @apply
   def mark( ):
      def fget(self):
         return self._mark
      def fset(self, arg):
         assert arg is None or isinstance(arg, str)
         self._mark = arg
      return property(**locals( ))
