from abjad.core.interface import _Interface
from abjad.rational.rational import Rational

class _OffsetInterface(_Interface):

   def __init__(self, _client):
      _Interface.__init__(self, _client)

   ### NOTE: try these tests on the context offsets:
   ###v = Voice(Note(1, (1,1))*900)
   ###t1 = Timer('v[-1].offset.context', 'from __main__ import v')
   ###print t1.timeit(6)
   ###t2 = Timer('v[-1].offset.context2', 'from __main__ import v')
   ###print t2.timeit(6)
   ###t3 = Timer('v[-1].offset.context3', 'from __main__ import v')
   ###print t3.timeit(6)

   @property
   def context(self):
      prev = self._client._navigator._prev
      if prev and prev._parentage._threadParentage == \
            self._client._parentage._threadParentage:
         result = prev.offset.context + prev.duration.prolated 
      else:
         result = Rational(0, 1)
      return result         

   ### NOTE: [VA] since no recursion is used there, we do not have the
   ### problem of reaching maximum recursion depth. so this is fixed here.
   ### hovever, there is no gain in computation time. 
   @property
   def context2(self):
      offset = Rational(0, 1)
      prev = self._client._navigator._prev
      self_parentage = self._client._parentage._threadParentage
      if not prev:
         return Rational(0, 1)
      while prev and prev._parentage._threadParentage == self_parentage:
         offset += prev.duration.prolated
         prev = prev._navigator._prev
      return offset 

   ### NOTE: [VA] can't quite figure out how to make the tail recursion 
   ### work. here we are keeping track of the result, but the problem is that
   ### we still need to compute the prev leaves withing the auxiliary
   ### method (i think) bringing us back to the maximum recursion depth problem.
   ### so context3 is no improvement over context.
   @property
   def context3(self):
      return self._offset_auxiliary(self._client)

   def _offset_auxiliary(self, current, result = Rational(0, 1)):
      prev = current._navigator._prev
      if not prev:
         return result
      elif prev and prev._parentage._threadParentage == \
            self._client._parentage._threadParentage:
         dur = prev.duration.prolated 
         return self._offset_auxiliary(prev, dur + result)


   @property
   def score(self):
      prev = self._client._navigator._prev
      if prev:
         result = prev.offset.score + prev.duration.prolated 
      else:
         result = Rational(0, 1)
      return result

   @property
   def newScore(self):
      total = Rational(0)
      g = self._client._navigator._depthFirstRightToLeft( )
      for x in g:
         if x.kind('_Leaf'):
            total += x.duration.prolated
      return total
