from abjad.containers.container import Container
from abjad.helpers.leaf_scale import leaf_scale
from abjad.helpers.leaf_split import leaf_split
from abjad.leaf.leaf import _Leaf
from abjad.duration.rational import Rational


def scopy(expr, start = 0, stop = None):
   '''Docs go here.'''

   if isinstance(expr, _Leaf):
      return _scopy_leaf(expr, start, stop)
   elif isinstance(expr, Container):
      return _scopy_container(expr, start, stop)
   else:
      raise ValueError('must be leaf or container.')


# t = Staff(Note(0, (1, 8)) * 4)
# Beam(t)
# new = scopy(t[0], (1, 16), (2, 16))
# new is like c'16 [ ] and t remains untouched

# boundary cases with t = Note(0, (1, 4))
# scopy(t, 0, (1, 2)); copy whole thing
# scopy(t, (1, 2), (3, 4)); return None
# scopy(t, (1, 16), (5, 16)); copy from (1, 16) to end-of-note == (4, 16)
# scopy(t, (1, 16), (100, 16)); ditto
# scopy(t, (2, 16), (3, 16)); copy from (2, 16) to (3, 16) for dur == (1, 16)
def _scopy_leaf(leaf, start, stop):
   if isinstance(start, (list, tuple)):
      start = Rational(*start)
   if isinstance(stop, (list, tuple)):
      stop = Rational(*stop)
   assert stop >= start
   
   # TODO - check leaf.duration versus leaf.duration.prolated
   if start >= leaf.duration.prolated:
      return None

   if start < 0:
      start = Rational(0)

   if stop > leaf.duration.prolated:
      stop = leaf.duration.prolated
   total = stop - start

   if total == 0:
      return None

   new = leaf.copy( )
   new = leaf_scale(total, new)
   return new



def _scopy_container(container, start, stop):
   pass
