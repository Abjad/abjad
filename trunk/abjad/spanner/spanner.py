from abjad.component.component import _Component
from abjad.core.abjadcore import _Abjad
from abjad.helpers.hasname import hasname
from abjad.helpers.instances import instances
from abjad.rational.rational import Rational
from copy import copy as python_copy


class Spanner(_Abjad):

   def __init__(self, music = None):
      self._components = [ ]
      if isinstance(music, (tuple, list)):
         self.extend(music)
      elif hasname(music, '_Component'):
         self.append(music)

   ### OVERLOADS ###

   def __contains__(self, expr):
      return self._components.__contains__(expr)

   def __delitem__(self, expr):
      if isinstance(expr, int):
         self.remove(self.components[expr])
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

   ### PRIVATE ATTRIBUTES ###

   @property
   def _summary(self):
      if len(self.components) > 0:
         return ', '.join([str(x) for x in self.components])
      else:
         return ' '

   ### PRIVATE METHODS ###

   def _after(self, component):
      return [ ]

   def _before(self, component):
      return [ ]

   def _blockByReference(self, component):
      component.spanners._spanners.remove(self)

#   def _block(self, i = None, j = None):
#      if i is not None and j is None:
#         component = self.components[i]
#         self._blockByReference(component)
#      elif i is not None and j is not None:
#         for component in self.components[i : j + 1]:
#            self._blockByReference(component)
#      else:
#         for component in self.components:
#            self._blockByReference(component)

   def _blockAll(self):
      for component in self.components:
         self._blockByReference(component)

   def _durationOffsetInMe(self, leaf):
      leaves = self.leaves
      assert leaf in leaves
      prev = leaves[ : leaves.index(leaf)]
      return sum([leaf.duration.prolated for leaf in prev])

   def _fractureLeft(self, i):
      left = self.copy(0, i - 1)
      right = self.copy(i, len(self.components))
      self._blockAll( )
      return self, left, right

   def _fractureRight(self, i):
      left = self.copy(0, i)
      right = self.copy(i + 1, len(self.components))
      self._blockAll( )
      return self, left, right

   def _fuseByReference(self, spanner):
      result = self.copy( )
      result.extend(spanner.components)
      self._blockAll( )
      spanner._blockAll( )
      return [(self, spanner, result)]

   def _isMyFirstLeaf(self, leaf):
      leaves = self.leaves
      return leaves and leaf is leaves[0]
   
   def _isMyLastLeaf(self, leaf):
      leaves = self.leaves
      return leaves and leaf is leaves[-1]

   def _isMyOnlyLeaf(self, leaf):
      return self._isMyFirstLeaf(leaf) and self._isMyLastLeaf(leaf)

   def _isMyFirst(self, leaf, classname):
      if leaf.kind(classname):
         leaves = self.leaves
         i = leaves.index(leaf)
         for x in leaves[ : i]:
            if x.kind(classname):
               return False
         return True
      return False

   def _isMyLast(self, leaf, classname):
      if leaf.kind(classname):
         leaves = self.leaves
         i = leaves.index(leaf)
         for x in leaves[i + 1 : ]:
            if x.kind(classname):
               return False
         return True
      return False

   def _isMyOnly(self, leaf, classname):
      return leaf.kind(classname) and len(self.leaves) == 1

   def _left(self, component):
      return [ ]

   def _right(self, component):
      return [ ]

#   def _remove(self, i = None, j = None):
#      if i is not None and j is None:
#         self._removeByReference(self.components[i])
#      elif i is not None and j is not None:
#         for component in self.components[i : j + 1]:
#            self._removeByReference(component)
#      else:
#         for component in self.components[ : ]:
#            self._removeByReference(component)

   def _removeByReference(self, component):
      self._components.remove(component)

#   def _sever(self, i = None, j = None):
#      if i is not None and j is None:
#         component = self.components[i]
#         self._severByReference(component)
#      elif i is not None and j is not None:
#         for n in reversed(range(i, j + 1)):
#            component = self.components[n]
#            self._severByReference(component)
#      else:
#         for n in reversed(range(len(self.components))):
#            component = self.components[n]
#            self._severByReference(component)

   def _severAll(self):
      for n in reversed(range(len(self.components))):
         component = self.components[n]
         self._severByReference(component)

   def _severByReference(self, component):
      self._blockByReference(component)
      self._removeByReference(component)

#   def _unblock(self, i = None, j = None):
#      if i is not None and j is None:
#         component = self.components[i]
#         self._unblockByReference(component)
#      elif i is not None and j is not None:
#         for component in self.components[i : j + 1]:
#            self._unblockByReference(component)
#      else:
#         for component in self.components:
#            self._unblockByReference(component)

   def _unblockAll(self):
      for component in self.components:
         self._unblockByReference(component)

   def _unblockByReference(self, component):
      if self not in component.spanners._spanners:
         component.spanners._append(self)

   ### PUBLIC ATTRIBUTES ###
   
   @property
   def components(self):
      return self._components[ : ]

   @property
   def duration(self):
      return sum([l.duration.prolated for l in self.components])

   @property
   def leaves(self):
      result = [ ]
      for component in self._components:
         for node in component._navigator._DFS(forbid = 'Parallel'):
            if node.kind('_Leaf'):
               result.append(node)
      return result

   ### PUBLIC METHODS ###

   def append(self, component):
      assert isinstance(component, _Component)
      self.insert(len(self.components), component)

   def copy(self, start = None, stop = None):
      result = python_copy(self)
      result._components = [ ]
      if stop is not None:
         for component in self.components[start : stop + 1]:
            result._components.append(component)
      else:
         for component in self.components:
            result._components.append(component)
      result._unblockAll( )
      return result

   def clear(self):
      self._severAll( )

   def extend(self, music):
      assert isinstance(music, (tuple, list))
      for component in music:
         assert isinstance(component, _Component)
         self.append(component)

   def fracture(self, i, direction = 'both'):
      if i < 0:
         i = len(self.components) + i
      if direction == 'left':
         return self._fractureLeft(i)
      elif direction == 'right':
         return self._fractureRight(i)
      elif direction == 'both':
         left = self.copy(0, i - 1)
         right = self.copy(i + 1, len(self.components))
         center = self.copy(i, i)
         self._blockAll( )
         return self, left, center, right
      else:
         raise ValueError(
            'direction %s must be left, right or both.' % direction)

   def fuse(self, spanner):
      return self._fuseByReference(spanner)
      
   def index(self, component):
      return self._components.index(component)

   def insert(self, i, component):
      component.spanners._spanners.append(self)
      self._components.insert(i, component)

   def pop(self, i = -1):
      component = self.components[i]
      self._severByReference(component)
      return component

   def remove(self, component):
      self._severByReference(component)
