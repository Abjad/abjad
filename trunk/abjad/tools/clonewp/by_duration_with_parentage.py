from abjad.component import _Component
from abjad.container import Container
from abjad.leaf import _Leaf
from abjad.rational import Rational
from abjad.tools import durtools
from abjad.tools import iterate
from abjad.tools import leaftools
from abjad.tools import split
from abjad.tools.clone.fracture import fracture
from abjad.tools.clonewp.by_leaf_range_with_parentage import \
   by_leaf_range_with_parentage


def by_duration_with_parentage(expr, start = 0, stop = None):
   r'''Clone `expr` from `start` to `stop` with parentage. ::

      abjad> voice = Voice(construct.run(2))
      abjad> voice.append(FixedDurationTuplet((2, 8), construct.run(3)))
      abjad> pitchtools.diatonicize(voice)
      abjad> f(voice)
      \new Voice {
        c'8
        d'8
        \times 2/3 {
                e'8
                f'8
                g'8
        }
      }
      
   ::
      
      abjad> new = clonewp.by_duration_with_parentage(voice, (0, 8), (3, 8))
      abjad> f(new)
      \new Voice {
        c'8
        d'8
        \times 2/3 {
                e'8
                f'16
        }
      }

   Raise contiguity error if asked to slice a parallel container. ::

      abjad> staff = Staff(Voice(construct.scale(2)) * 2)
      abjad> staff.parallel = True
      abjad> f(staff)
      \new Staff <<
        \new Voice {
                c'8
                d'8
        }
        \new Voice {
                c'8
                d'8
        }
      >>
      abjad> clonewp.by_duration_with_parentage(staff, 0, (1, 8))
      ContiguityError

   .. note:: cases with ``0 = start`` work correctly.

   ::

      abjad> new = clonewp.by_duration_with_parentage(voice, (0, 8), (1, 8))
      abjad> f(new)
      \new Voice {
        c'8
      }
      
   .. note:: cases with ``0 < start`` do not work correctly.

   ::
      
      abjad> new = clonewp.by_duration_with_parentage(voice, (1, 8), (2, 8))
      abjad> f(new)
      \new Voice {
        c'8
        d'8
      }

   .. note:: function creates ad hoc tuplets as required.

   ::

      abjad> voice = Voice([Note(0, (1, 4))])
      abjad> new = clonewp.by_duration_with_parentage(voice, 0, (1, 12))
      abjad> f(new)
      \new Voice {
        \times 2/3 {
                c'8
        }
      }
   '''

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
   new = fracture([leaf])[0]
   leaftools.duration_preprolated_change(new, total)
   return new


def _scopy_container(container, start, stop):
   container, first_dif, second_dif = _get_lcopy(container, start, stop)
   #print first_dif, second_dif
   leaf_start = container.leaves[0]
   leaf_end = container.leaves[-1]
   # split first leaf
   #leaf_start_splitted = split.leaf_at_duration(leaf_start, first_dif)
   leaf_start_splitted = split.unfractured_at_duration(leaf_start, first_dif)
   if len(leaf_start_splitted) == 2:
      leaftools.excise(leaf_start_splitted[0][0])
   # split second leaf
   #leaf_end_splitted = split.leaf_at_duration(leaf_end, second_dif)
   leaf_end_splitted = split.unfractured_at_duration(leaf_end, second_dif)
   if len(leaf_end_splitted) == 2:
      leaftools.excise(leaf_end_splitted[1][0])
   return container


def _get_lcopy(container, start, stop):
   total_dur = Rational(0)
   start_leaf, stop_leaf = None, None
   first_dif = second_dif = 0
   for i, leaf in enumerate(iterate.leaves_forward_in(container)):
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
   untrimmed_copy = by_leaf_range_with_parentage(
      container, start_leaf, stop_leaf)
   return untrimmed_copy, first_dif, second_dif
