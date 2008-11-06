from abjad.core.attributeformatter import _AttributeFormatter
from abjad.core.interface import _Interface
from abjad.core.spannerreceptor import _SpannerReceptor

### TODO - make composer interface decisions about whether to support
###        _DynamicsInterface.effective or not, and, if so, how.

#class _DynamicsInterface(_Interface):
class _DynamicsInterface(_Interface, _AttributeFormatter, _SpannerReceptor):
   
   def __init__(self, client):
      #_Interface.__init__(self, client, 'DynamicText', 
      #   ['Crescendo', 'Decrescendo'])
      _Interface.__init__(self, client)
      _AttributeFormatter.__init__(self, 'DynamicText')
      _SpannerReceptor.__init__(self, ['Crescendo', 'Decrescendo'])
      self._mark = None

   ### OVERRIDES ###

   def __nonzero__(self):
      return bool(self._mark)

   def __eq__(self, arg):
      assert isinstance(arg, bool)
      return bool(self._mark) == arg

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

#   def __repr__(self):
#      return '_DynamicsInterface(%s)' % self._summary

   ### DERIVED PROPERTIES ###

   @property
   def effective(self):
      if self.spanner:
         return self.spanner
      else:
         if self.mark:
            return self.mark
         else:
            cur = self._client.prev
            while cur:
               if cur.dynamics.spanner:
                  return cur.dynamics.spanner.stop
               elif cur.dynamics.mark:
                  return cur.dynamics.mark
               else:
                  cur = cur.prev
            return None

   ### MANAGED ATTRIBUTES ###

   @apply
   def mark( ):
      def fget(self):
         return self._mark
      def fset(self, arg):
         if arg is None:
            self._mark = arg
         elif isinstance(arg, str):
            self._mark = arg
         else:
            raise ValueError('dynamics %s must be str or None.' % str(arg))
      return property(**locals( ))

   ### FORMATTING ###

   @property
   def _right(self):
      result = [ ]
      if self.mark:
         result.append(r'\%sX' % self.mark)
      return result
