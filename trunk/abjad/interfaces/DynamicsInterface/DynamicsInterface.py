from abjad.core import _FormatContributor
from abjad.interfaces._Interface import _Interface


class DynamicsInterface(_Interface, _FormatContributor):
   '''Implement read / write 'mark' attribute.
   '''
   
   def __init__(self, client):
      _Interface.__init__(self, client)
      _FormatContributor.__init__(self)
      self._mark = None

   ## PRIVATE ATTRIBUTES ##

   @property
   def _summary(self):
      '''Summary of contents as string.'''
      from abjad.tools import spannertools
      result = [ ]
      spanners = spannertools.get_all_spanners_attached_to_component(self._client,
         (spannertools.DynamicTextSpanner, spannertools.HairpinSpanner))
      if self.mark:
         result.append(self.mark)
      if 0 < len(spanners):
         result.append(spanners[0])
      if result:
         return ', '.join([str(x) for x in result])
      else:
         return ' '

   ## PUBLIC ATTRIBUTES ##

   @property
   def effective(self):
      '''Effective dynamic.'''
      from abjad.components.Container import Container
      from abjad.tools.spannertools import DynamicTextSpanner
      from abjad.tools.spannertools import HairpinSpanner
      from abjad.tools import spannertools
      if isinstance(self._client, Container):
         return None
      if self.mark:
         return self.mark
      spanners = spannertools.get_all_spanners_attached_to_component(self._client,
         (DynamicTextSpanner, HairpinSpanner))
      if 0 < len(spanners):
         spanner = spanners.pop( )
         if isinstance(spanner, DynamicTextSpanner):
            return spanner.mark
         elif isinstance(spanner, HairpinSpanner):
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
