from abjad.core import _FormatContributor
from abjad.core import _GrobHandler
from abjad.interfaces._Interface import _Interface
from abjad.marks import Articulation


class ArticulationInterface(_Interface, _GrobHandler):
   '''Handle the LilyPond Script grob.'''

   def __init__(self, client):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Script')
      self._articulations = [ ]

   ## OVERLOADS ##

   def __contains__(self, expr):
      expr = self._make_articulation(expr)
      for a in self._articulations:
         if expr == a:
            return True
      return False

   def __delitem__(self, i):
      del(self._articulations[i])

   def __getitem__(self, expr):
      return self._articulations[expr]

   def __len__(self):
      return len(self._articulations)

   def __repr__(self):
      if len(self._articulations):
         return '<ArticulationInterface(%s)>' % ', '.join([str(x) 
            for x in self._articulations])
      else:
         return '<ArticulationInterface>'

   def __setitem__(self, i, expr):
      if isinstance(i, int):
         if i < 0:
            j = len(self) + i
         else:
            j = i
         expr = self._make_articulation(expr)
         self._articulations[j] = expr 
      # slice
      else:
         assert isinstance(expr, list)
         expr = [self._make_articulation(x) for x in expr]
         self._articulations[i.start : i.stop] = expr

   ## PRIVATE METHODS ##

   def _make_articulation(self, expr):
      if isinstance(expr, Articulation):
         return expr
      elif isinstance(expr, (list, tuple)):
         return Articulation(*expr)
      elif isinstance(expr, str):
         return Articulation(expr)
      else:
         raise ValueError('can not create Articulation.')

   ## PUBLIC ATTRIBUTES ##

   @property
   def _right(self):
      '''Format contribution to right of leaf.'''
      result = [ ]
      result.extend([x.format for x in self._articulations])
      return result

   ## PUBLIC METHODS ##

   def append(self, expr):
      expr = self._make_articulation(expr)
      self._articulations.append(expr)

   def extend(self, expr):
      expr = [self._make_articulation(x) for x in expr]
      self._articulations.extend(expr)

   def insert(self, i, expr):
      expr = self._make_articulation(expr)
      self._articulations.insert(i, expr)

   def pop(self, i = -1):
      return self._articulations.pop(i)
      
   def remove(self, expr):
      expr = self._make_articulation(expr)
      for a in self._articulations:
         if expr == a:
            self._articulations.remove(a)

   def sort(self):
      def cmp(x, y):
         if x.string < y.string:
            return -1
         elif x.string > y.string:
            return 1
         else:
            return 0
      self._articulations.sort(cmp)
