from abjad.component.component import _Component
from abjad.container.container import Container
from abjad.helpers.excise import excise
from abjad.leaf.leaf import _Leaf
from abjad.rational.rational import Rational
from abjad.tools import clone
from abjad.tools import durtools
from abjad.tools import iterate
from abjad.tools import leaftools


def scopy(expr, start = 0, stop = None):
   '''Copy expr from start duration stop up to
      and including stop duration stop;
      slice all layers of structure as required.'''
   assert isinstance(expr, _Component)
   start = Rational(*durtools.token_unpack(start))
   if start < 0:
      start = Rational(0)
   if stop is None:
      stop = expr.duration.prolated
   else:
      stop = Rational(*durtools.token_unpack(stop))
   assert start <= stop
   if isinstance(expr, _Leaf):
      return _scopy_leaf(expr, start, stop)
   elif isinstance(expr, Container):
      return _scopy_container(expr, start, stop)
   else:
      raise ValueError('must be leaf or container.')


def _scopy_leaf(leaf, start, stop):
   if start >= leaf.duration.prolated:
      return None
   if stop > leaf.duration.prolated:
      stop = leaf.duration.prolated
   total = stop - start
   if total == 0:
      return None
   new = clone.fracture([leaf])[0]
   new = leaftools.scale(new, total)
   return new


def _scopy_container(container, start, stop):
   container, first_dif, second_dif = _get_lcopy(container, start, stop)
   #print first_dif, second_dif
   leaf_start = container.leaves[0]
   leaf_end = container.leaves[-1]
   # split first leaf
   leaf_start_splitted = leaftools.split(leaf_start, first_dif)
   if len(leaf_start_splitted) == 2:
      excise(leaf_start_splitted[0])
   # split second leaf
   leaf_end_splitted = leaftools.split(leaf_end, second_dif)
   if len(leaf_end_splitted) == 2:
      excise(leaf_end_splitted[1])
   return container


def _get_lcopy(container, start, stop):
   total_dur = Rational(0)
   start_leaf, stop_leaf = None, None
   first_dif = second_dif = 0
   from abjad.leaf.leaf import _Leaf
   for i, leaf in enumerate(iterate.naive(container, _Leaf)):
      total_dur += leaf.duration.prolated
      if total_dur == start and start_leaf is None:
         start_leaf = i
         first_dif = 0
      elif total_dur > start and start_leaf is None:
         start_leaf = i
         first_dif = leaf.duration.prolated - (total_dur - start)
         #print first_dif
      if total_dur >= stop and stop_leaf is None:
         stop_leaf = i + 1
         #second_dif = leaf.duration.prolated - (total_dur - stop)
         flamingo = total_dur - stop
         if flamingo != 0:
            second_dif = leaf.duration.prolated - flamingo
         #print second_dif
         #print 'breaking after stop'
         break
   #print start_leaf, stop_leaf
   untrimmed_copy = leaftools.copy_with_parentage(
      container, start_leaf, stop_leaf)
   return untrimmed_copy, first_dif, second_dif
