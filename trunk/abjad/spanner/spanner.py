from abjad.component.component import _Component
from abjad.core.abjadcore import _Abjad
from abjad.helpers.assert_components import assert_components
from abjad.helpers.iterate import iterate
from abjad.leaf.leaf import _Leaf
from abjad.spanner.duration import _SpannerDurationInterface
from abjad.rational.rational import Rational
from copy import copy as python_copy


class Spanner(_Abjad):

   def __init__(self, music = None):
      from abjad.component.component import _Component
      self._components = [ ]
      self._duration = _SpannerDurationInterface(self)
      self._initializeMusic(music)

   ## OVERLOADS ##

   def __contains__(self, expr):
      return self._components.__contains__(expr)

   def __getitem__(self, expr):
      return self._components.__getitem__(expr)

   def __len__(self):
      return self._components.__len__( )

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
  
   def _initializeMusic(self, music):
      music = music or [ ]
      if isinstance(music, _Component):
         music = [music]
      leaves = list(iterate(music, _Leaf))
      assert_components(leaves, contiguity = 'thread')
      self.extend(music)

   def _insert(self, i, component):
      '''Insert component in spanner at index i.
         Not composer-safe and may mangle spanners.'''
      component.spanners._add(self)
      self._components.insert(i, component)

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

   def _remove(self, component):
      '''Remove 'component' from spanner.
         Remove spanner from component's aggregator.
         Not composer-safe and may leave discontiguous spanners.'''
      self._severComponent(component)

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
      component.spanners._add(self)

   ## PUBLIC ATTRIBUTES ##
   
   @property
   def begin(self):
      '''Start time of first component in spanner.'''
      if len(self) > 0:
         return self[0].offset.score

   @property
   def components(self):
      return self._components[:]

   @property
   def duration(self):
      return self._duration
   
   @property
   def end(self):
      if len(self) > 0:
         last = self[-1]
         return last.offset.score + last.duration.prolated

   @property
   def leaves(self):
      from abjad.leaf.leaf import _Leaf
      result = [ ]
      for component in self._components:
         for node in component._navigator._DFS(forbid = 'parallel'):
            if isinstance(node, _Leaf):
               result.append(node)
      return result

   ## PUBLIC METHODS ##

   def append(self, component):
      components = self[-1:] + [component]
      assert_components(components, contiguity = 'thread')
      component.spanners._add(self)
      self._components.append(component)

   def append_left(self, component):
      components = [component] + self[:1] 
      assert_components(components, contiguity = 'thread')
      component.spanners._add(self)
      self._components.insert(0, component)

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

   def extend(self, components):
      input = self[-1:] + components
      assert_components(input, contiguity = 'thread')
      for component in components:
         self.append(component)

   def extend_left(self, components):
      input = components + self[:1]
      assert_components(input, contiguity = 'thread')
      for component in reversed(components):
         self.append_left(component)

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

   def pop(self):
      component = self[-1]
      self._severComponent(component)
      return component

   def pop_left(self):
      component = self[0]
      self._severComponent(component)
      return component

   def trim(self, component):
      assert component in self
      result = [ ]
      while not result[:1] == [component]:
         result.insert(0, self.pop( ))
      return result 

   def trim_left(self, component):
      assert component in self
      result = [ ]
      while not result[-1:] == [component]:
         result.append(self.pop( ))
      return result 
