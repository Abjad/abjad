from abjad.core.grobhandler import _GrobHandler
from abjad.interfaces.interface.interface import _Interface
from abjad.spanners import Dynamic
from abjad.spanners import Hairpin
from abjad.interfaces.spanner_receptor.receptor import _SpannerReceptor


## TODO: Dynamics by spanner only? ##
## TODO: Multistage dynamic spanner? ##

class DynamicsInterface(_Interface, _GrobHandler, _SpannerReceptor):
   '''Handle LilyPond DynamicText grob.
      Receive Abjad Dynamic and Hairpin spanners.
      Implement read / write 'mark' attribute.'''
   
   def __init__(self, client):
      '''Bind client, LilyPond DynamicText grob.
         Receive Abjad Dynamic and Hairpin spanners.
         Set 'mark' to None.'''
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'DynamicText')
      _SpannerReceptor.__init__(self, (Dynamic, Hairpin))
      self._mark = None

   ## PRIVATE ATTRIBUTES ##

   @property
   def _summary(self):
      '''Summary of contents as string.'''
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
      '''Effective dynamic.'''
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
      '''Read / write dynamic mark attaching to client.'''
      def fget(self):
         return self._mark
      def fset(self, arg):
         assert arg is None or isinstance(arg, str)
         self._mark = arg
      return property(**locals( ))

   @property
   def _right(self):
      '''Format contribution to right of leaf.'''
      result = [ ]
      if self.mark:
         result.append(r'\%s' % self.mark)
      return result
