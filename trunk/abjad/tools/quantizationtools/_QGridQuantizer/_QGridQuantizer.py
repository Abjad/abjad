from collections import Iterable
from itertools import groupby
from abjad import Fraction
from abjad.tools.contexttools import TempoMark
from abjad.tools.durtools import is_binary_rational
from abjad.tools.quantizationtools.tempo_scaled_rational_to_milliseconds \
   import tempo_scaled_rational_to_milliseconds
from abjad.tools.quantizationtools._Quantizer import _Quantizer
from abjad.tools.quantizationtools.QGridSearchTree import QGridSearchTree


class _QGridQuantizer(_Quantizer):

   __slots__ = ('_beatspan', '_beatspan_ms', '_q_grids',
      '_q_grid_tempo_lookup', '_search_tree', '_tempo', '_threshold')

   def __init__(self,
      search_tree = None,
      beatspan = Fraction(1, 4),
      tempo = TempoMark(Fraction(1, 4), 60),
      threshold = None):

      if search_tree is None:
         search_tree = QGridSearchTree( )
      else:
         assert isinstance(search_tree, QGridSearchTree)

      assert is_binary_rational(beatspan)
      if isinstance(beatspan, Fraction):
         assert beatspan.numerator == 1

      assert isinstance(tempo, TempoMark)

      if threshold is not None:
         assert 0 < threshold
         search_tree = search_tree.prune(tempo, threshold, beatspan)

      object.__setattr__(self, '_beatspan', beatspan)
      object.__setattr__(self, '_beatspan_ms', 
         tempo_scaled_rational_to_milliseconds(beatspan, tempo))
      object.__setattr__(self, '_q_grids', None) # lazy load
      object.__setattr__(self, '_q_grid_tempo_lookup', None) # lazy load
      object.__setattr__(self, '_search_tree', search_tree)
      object.__setattr__(self, '_tempo', tempo)
      object.__setattr__(self, '_threshold', threshold)

   ## PRIVATE METHODS ##

   def _find_nearest_q_grid_point_to_timepoint(self, timepoint, q_grid):
      best_point = q_grid[0]
      best_error = abs(self.q_grid_tempo_lookup[q_grid[0]] - timepoint)
      for q in q_grid[1:]:
         curr_error = abs(self.q_grid_tempo_lookup[q] - timepoint)
         if curr_error < best_error:
            best_point = q
            best_error = curr_error
      return best_point, best_error

   ## PUBLIC ATTRIBUTES ##

   @property
   def beatspan(self):
      return self._beatspan

   @property
   def beatspan_ms(self):
      return self._beatspan_ms

   @property
   def q_grids(self):
      if self._q_grids is None:
         object.__setattr__(self, '_q_grids',
            tuple([x.q_grid * self.beatspan
               for x in self.search_tree.rhythm_trees]))
      return self._q_grids

   @property
   def q_grid_tempo_lookup(self):
      if self._q_grid_tempo_lookup is None:
         q_grid_tempo_lookup = { }
         for q_grid in self.q_grids:
            for q in q_grid:
               if q not in q_grid_tempo_lookup:
                  q_grid_tempo_lookup[q] = \
                     int(tempo_scaled_rational_to_milliseconds(q, self.tempo))
         object.__setattr__(self, '_q_grid_tempo_lookup', q_grid_tempo_lookup)
      return self._q_grid_tempo_lookup

   @property
   def rhythm_trees(self):
      return self._search_tree.rhythm_trees

   @property
   def search_tree(self):
      return self._search_tree

   @property
   def tempo(self):
      return self._tempo

   @property
   def threshold(self):
      return self._threshold
