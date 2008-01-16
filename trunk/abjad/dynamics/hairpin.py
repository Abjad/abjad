from .. core.spanner import _Spanner

class _Hairpin(_Spanner):

   def __init__(self, leaves, fit = None):
      _Spanner.__init__(self, leaves)
      self.fit = fit

   def __str__(self):
      result = [ ]
      if len(self) > 0:
         if self.leaves[0].dynamics.mark:
            result.append(self.leaves[0].dynamics.mark)
         result.append(self._body)
         if self.leaves[-1].dynamics.mark:
            result.append(self.leaves[-1].dynamics.mark)
         return ' '.join([str(x) for x in result])
      else:
         return self._body

   @property
   def start(self):
      if len(self) > 0:
         return self.leaves[0].dynamics.mark

   @property
   def stop(self):
      if len(self) > 0:
         return self.leaves[-1].dynamics.mark

   def _right(self, leaf):
      result = [ ]
      if self.fit is None:
         if self._isMyFirstLeaf(leaf):
            result.append('\\%s' % self._shape)
         if self._isMyLastLeaf(leaf):
            if not leaf.dynamics.mark:
               result.append('\\!')
      elif self.fit is 'trim':
         if self._isMyFirst(leaf, ('Note', 'Chord')):
            result.append('\\%s' % self._shape)
         if self._isMyLast(leaf, ('Note', 'Chord')):
            if not leaf.dynamics.mark:
               result.append('\\!')
      else:
         raise ValueError('unknown hairpin type %s.' % str(self.type))
      return result


def Hairpin(leaves, *args, **kwargs):
   if len(args) == 1:
       start, shape, stop = None, args[0], None
   elif len(args) == 3:
      start, shape, stop = args
   else:
      raise ValueError('args %s must be len 1 or 3.' % str(args))
   if shape == '<':
      from crescendo import Crescendo
      result = Crescendo(leaves, **kwargs)
   elif shape == '>':
      from decrescendo import Decrescendo
      result = Decrescendo(leaves, **kwargs)
   if result.fit is None:
      if start:
         result.leaves[0].dynamics.mark = start
      if stop:
         result.leaves[-1].dynamics.mark = stop
   elif result.fit == 'trim':
      if start:
         for leaf in result.leaves:
            if result._isMyFirst(leaf, ('Note', 'Chord')):
               leaf.dynamics.mark = start
               break
      if stop:
         for leaf in reversed(result.leaves):
            if result._isMyLast(leaf, ('Note', 'Chord')):
               leaf.dynamics.mark = stop
               break
   return result

