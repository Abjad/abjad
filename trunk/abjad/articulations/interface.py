from abjad.articulations.articulation import _Articulation
from abjad.core.interface import _Interface

class _ArticulationsInterface(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client)
      self._articulations = [ ]

   def __repr__(self):
      if len(self._articulations):
         return 'Articulations(%s)' % ', '.join([str(x) 
            for x in self._articulations])
      else:
         return 'Articulations( )'

   ### FORMATTING ###

   @property
   def _right(self):
      result = [ ]
      result.extend([x.lily for x in self._articulations])
      return result

   ### MANAGEMENT ###

   def append(self, expr):
      expr = self._makeArticulation(expr)
      self._articulations.append(expr)

   def extend(self, expr):
      expr = [self._makeArticulation(x) for x in expr]
      self._articulations.extend(expr)

   def remove(self, expr):
      expr = self._makeArticulation(expr)
      for a in self._articulations:
         if expr == a:
            self._articulations.remove(a)

   def pop(self, i = -1):
      return self._articulations.pop(i)
      
   def insert(self, i, expr):
      expr = self._makeArticulation(expr)
      self._articulations.insert(i, expr)

   def sort(self):
      def cmp(x, y):
         if x.string < y.string:
            return -1
         elif x.string > y.string:
            return 1
         else:
            return 0
      self._articulations.sort(cmp)

   ### OVERRIDES ###

   def __len__(self):
      return len(self._articulations)

   def __contains__(self, expr):
      expr = self._makeArticulation(expr)
      for a in self._articulations:
         if expr == a:
            return True
      return False

   def __setitem__(self, i, expr):
      if isinstance(i, int):
         if i < 0:
            j = len(self) + i
         else:
            j = i
         expr = self._makeArticulation(expr)
         self._articulations[j] = expr 
      # slice
      else:
         assert isinstance(expr, list)
         expr = [self._makeArticulation(x) for x in expr]
         self._articulations[i.start : i.stop] = expr

   def __getitem__(self, expr):
      return self._articulations[expr]

   def __delitem__(self, i):
      del(self._articulations[i])

   ### UTILS ###

   def _makeArticulation(self, expr):
      if isinstance(expr, _Articulation):
         return expr
      elif isinstance(expr, (list, tuple)):
         return _Articulation(*expr)
      elif isinstance(expr, str):
         return _Articulation(expr)
      else:
         raise ValueError('can not create _Articulation.')
