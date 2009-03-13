from abjad.component.component import _Component
from abjad.core.abjadcore import _Abjad
from abjad.rational.rational import Rational
from copy import copy as python_copy


class Spanner(_Abjad):

   def __init__(self, music = None):
      from abjad.component.component import _Component
      self._components = [ ]
      if isinstance(music, (tuple, list)):
         self.extend(music)
      elif isinstance(music, _Component):
         self.append(music)

   ## OVERLOADS ##

   def __contains__(self, expr):
      return self._components.__contains__(expr)

   def __delitem__(self, expr):
      if isinstance(expr, int):
         self.remove(self[expr])
      elif isinstance(expr, slice):
         start, stop, stride = expr.indices(len(self))
         for i in reversed(range(start, stop, stride)):
            del(self[i])

   def __getitem__(self, expr):
      return self._components.__getitem__(expr)

   def __len__(self):
      return self._components.__len__( )

   def __setitem__(self, idx, expr):
      if isinstance(idx, int):
         if idx < 0:
            idx = len(self) + idx
         del(self[idx])
         self.insert(idx, expr)
      elif isinstance(idx, slice):
         assert isinstance(expr, (tuple, list))
         start, stop, stride = idx.indices(len(self))
         del(self[start : stop])
         for component in reversed(expr):
            self.insert(start, component)
         
   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._summary)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _summary(self):
      if len(self) > 0:
         return ', '.join([str(x) for x in self])
      else:
         return ' '

   ## PRIVATE METHODS ##

   def _after(self, component):
      return [ ]

   def _before(self, component):
      return [ ]

   def _blockAllComponents(self):
      for component in self:
         self._blockComponent(component)

   def _blockComponent(self, component):
      component.spanners._spanners.remove(self)

   def _durationOffsetInMe(self, leaf):
      leaves = self.leaves
      assert leaf in leaves
      prev = leaves[ : leaves.index(leaf)]
      return sum([leaf.duration.prolated for leaf in prev])

   def _fractureLeft(self, i):
      left = self.copy(0, i - 1)
      right = self.copy(i, len(self))
      self._blockAllComponents( )
      return self, left, right

   def _fractureRight(self, i):
      left = self.copy(0, i)
      right = self.copy(i + 1, len(self))
      self._blockAllComponents( )
      return self, left, right

   def _fuseByReference(self, spanner):
      result = self.copy( )
      result.extend(spanner.components)
      self._blockAllComponents( )
      spanner._blockAllComponents( )
      return [(self, spanner, result)]

   def _isMyFirstLeaf(self, leaf):
      leaves = self.leaves
      return leaves and leaf is leaves[0]
   
   def _isMyLastLeaf(self, leaf):
      leaves = self.leaves
      return leaves and leaf is leaves[-1]

   def _isMyOnlyLeaf(self, leaf):
      return self._isMyFirstLeaf(leaf) and self._isMyLastLeaf(leaf)

   def _isMyFirst(self, leaf, klass):
      if isinstance(leaf, klass):
         leaves = self.leaves
         i = leaves.index(leaf)
         for x in leaves[ : i]:
            if isinstance(x, klass):
               return False
         return True
      return False

   def _isMyLast(self, leaf, klass):
      if isinstance(leaf, klass):
         leaves = self.leaves
         i = leaves.index(leaf)
         for x in leaves[i + 1 : ]:
            if isinstance(x, klass):
               return False
         return True
      return False

   def _isMyOnly(self, leaf, klass):
      return isinstance(leaf, klass) and len(self.leaves) == 1

   def _left(self, component):
      return [ ]

   def _right(self, component):
      return [ ]

   def _removeComponent(self, component):
      self._components.remove(component)

   def _severAllComponents(self):
      for n in reversed(range(len(self))):
         component = self[n]
         self._severComponent(component)

   def _severComponent(self, component):
      self._blockComponent(component)
      self._removeComponent(component)

   def _unblockAllComponents(self):
      for component in self:
         self._unblockComponent(component)

   def _unblockComponent(self, component):
      component.spanners._update([self])

   ## PUBLIC ATTRIBUTES ##
   
   @property
   def components(self):
      return self._components[ : ]

   ## TODO: replace with _SpannerDurationInterface ##

   @property
   def duration(self):
      return sum([l.duration.prolated for l in self])

   @property
   def leaves(self):
      from abjad.container.parallel import Parallel
      from abjad.leaf.leaf import _Leaf
      result = [ ]
      for component in self._components:
         for node in component._navigator._DFS(forbid = Parallel):
            if isinstance(node, _Leaf):
               result.append(node)
      return result

   ## TODO: replace with _SpannerDurationInterface ##

   @property
   def written(self):
      return sum([l.duration.written for l in self])

   ## PUBLIC METHODS ##

   def append(self, component):
      assert isinstance(component, _Component)
      self.insert(len(self), component)

   def copy(self, start = None, stop = None):
      result = python_copy(self)
      result._components = [ ]
      if stop is not None:
         for component in self[start : stop + 1]:
            result._components.append(component)
      else:
         for component in self:
            result._components.append(component)
      result._unblockAllComponents( )
      return result

   def clear(self):
      self._severAllComponents( )

   def extend(self, music):
      assert isinstance(music, (tuple, list))
      for component in music:
         assert isinstance(component, _Component)
         self.append(component)

   def fracture(self, i, direction = 'both'):
      if i < 0:
         i = len(self) + i
      if direction == 'left':
         return self._fractureLeft(i)
      elif direction == 'right':
         return self._fractureRight(i)
      elif direction == 'both':
         left = self.copy(0, i - 1)
         right = self.copy(i + 1, len(self))
         center = self.copy(i, i)
         self._blockAllComponents( )
         return self, left, center, right
      else:
         raise ValueError(
            'direction %s must be left, right or both.' % direction)

   def fuse(self, spanner):
      return self._fuseByReference(spanner)
      
   def index(self, component):
      return self._components.index(component)

   def insert(self, i, component):
      component.spanners._update([self])
      self._components.insert(i, component)

   def pop(self, i = -1):
      component = self[i]
      self._severComponent(component)
      return component

   def remove(self, component):
      self._severComponent(component)
