from abjad.core.abjadcore import _Abjad
from abjad.helpers.instances import instances
from abjad.rational.rational import Rational
from copy import copy as python_copy


### TODO - Take away the ability to take len(p) and to iterate p.
###        Force explicit len(p.leaves), len(p.components) instead.

class Spanner(_Abjad):

   def __init__(self, music):
      self._components = [ ]
      self._extend(music)

   ### OVERLOADS ###

   def __contains__(self, arg):
      return arg in self._components 

   def __getitem__(self, arg):
      if isinstance(arg, (int, slice)):
         return self._components[arg]
      else:
         raise TypeError('spanner indices must be integers.')

   def __len__(self):
      return len(self._components)

   def __repr__(self):
      try:
         return self.before(self[0])[0]
      except:
         return '%s(%s)' % (self.__class__.__name__, self._summary)

   ### PRIVATE ATTRIBUTES ###

   @property
   def _summary(self):
      if len(self) > 0:
         return ', '.join([str(x) for x in self])
      else:
         return ' '

   ### PRIVATE METHODS ###

   def _after(self, component):
      return [ ]

   def _append(self, component):
      self._insert(len(self), component)

   def _before(self, component):
      return [ ]

   #def _blockByReference(self, leaf):
   #   leaf.spanners._spanners.remove(self)
   def _blockByReference(self, component):
      component.spanners._spanners.remove(self)

   def _block(self, i = None, j = None):
      if i is not None and j is None:
         #leaf = self[i]
         #self._blockByReference(leaf)
         component = self.components[i]
         self._blockByReference(component)
      elif i is not None and j is not None:
         #for leaf in self[i : j + 1]:
         #   self._blockByReference(leaf)
         for component in self.components[i : j + 1]:
            self._blockByReference(component)
      else:
         #for leaf in self:
         #   self._blockByReference(leaf)
         for component in self.components:
            self._blockByReference(component)

   def _durationOffsetInMe(self, leaf):
      #assert leaf in self
      #prev = self[ : self.index(leaf)]
      #return sum([leaf.duration.prolated for leaf in prev])
      leaves = self.leaves
      assert leaf in leaves
      prev = leaves[ : leaves.index(leaf)]
      return sum([leaf.duration.prolated for leaf in prev])

   def _extend(self, music):
      if isinstance(music, (tuple, list)):
         for component in music:
            self._append(component)
      elif music.kind('_Component'):
         self._append(music)
      else:
         raise ValueError('can only span components.')

   def _follows(self, spanner):
      return spanner[-1].next == self[0]

   def _fractureLeft(self, i):
      left = self.copy(0, i - 1)
      right = self.copy(i, len(self))
      self._block( )
      return self, left, right

   def _fractureRight(self, i):
      left = self.copy(0, i)
      right = self.copy(i + 1, len(self))
      self._block( )
      return self, left, right

   def _fuseByReference(self, spanner):
      if self._matches(spanner) and spanner._follows(self):
         result = self.copy( )
         #result._extend(spanner)
         result._extend(spanner.components)
         self._block( )
         spanner._block( )
         return [(self, spanner, result)]
      else:
         return [ ]

   def _fuseRight(self):
      result = [ ]
      if self._matchingSpannerAfterMe( ):
         result.extend(self._fuseByReference(self._matchingSpannerAfterMe( )))
      return result

   def _fuseLeft(self):
      result = [ ]
      if self._matchingSpannerBeforeMe( ):
         result.extend(self._matchingSpannerBeforeMe( )._fuseByReference(self))
      return result

   def _insert(self, i, component):
      component.spanners._spanners.append(self)
      self._components.insert(i, component)

   def _isMyFirstLeaf(self, leaf):
      #return len(self) > 0 and leaf == self[0]
      leaves = self.leaves
      return leaves and leaf is leaves[0]
   
   def _isMyLastLeaf(self, leaf):
      #return len(self) > 0 and leaf == self[-1]
      leaves = self.leaves
      return leaves and leaf is leaves[-1]

   def _isMyOnlyLeaf(self, leaf):
      return self._isMyFirstLeaf(leaf) and self._isMyLastLeaf(leaf)

   def _isMyFirst(self, leaf, classname):
      if leaf.kind(classname):
         leaves = self.leaves
         #i = self.index(leaf)
         i = leaves.index(leaf)
         #for x in self[ : i]:
         for x in leaves[ : i]:
            if x.kind(classname):
               return False
         return True
      return False

   def _isMyLast(self, leaf, classname):
      if leaf.kind(classname):
         leaves = self.leaves
         #i = self.index(leaf)
         i = leaves.index(leaf)
         #for x in self[i + 1 : ]:
         for x in leaves[i + 1 : ]:
            if x.kind(classname):
               return False
         return True
      return False

   def _isMyOnly(self, leaf, classname):
      #return leaf.kind(classname) and len(self) == 1
      return leaf.kind(classname) and len(self.leaves) == 1

   def _left(self, component):
      return [ ]

   ### TODO - consider implementing a dedicated attribute comparison method
   ###        to work on any two spanners;
   ###        such a method would feed into _matches( ), below.

   ### TODO - figure out if we really need the attribute check or not;
   ###        looks like the attribute check doesn't work right now,
   ###        at least not for two different octavation spanners.

   def _matches(self, spanner):
      return self.__class__ == spanner.__class__ and \
         all([getattr(self, attr, None) == getattr(spanner, attr, None)
            for attr in ('_grob', '_attribute', '_value')])

   ### TODO - _matchingSpanner( ) functions as a generalization of
   ###        _matchingSpannerBeforeMe( ) and _matchingSpannerAfterMe( );
   ###        cleaner to reimplement _matchingSpanner( ) completely
   ###        independently of those two functions 
   ###        and then eliminate those two functions entirely;
   ###        this will take us from three functions 
   ###        down to only _matchingSpanner( ).

   def _matchingSpanner(self, direction):
      assert direction in ('left', 'right')
      if direction == 'left':
         return self._matchingSpannerBeforeMe( )
      else:
         return self._matchingSpannerAfterMe( )

   def _matchingSpannerAfterMe(self):
      if self[-1].next:
         matches = self[-1].next.spanners.get(
            #interface = getattr(self, '_interface', None),
            grob = getattr(self, '_grob', None),
            attribute = getattr(self, '_attribute', None),
            value = getattr(self, '_vallue', None))
         if matches:
            return matches[0]

   def _matchingSpannerBeforeMe(self):
      if self[0].prev:
         matches = self[0].prev.spanners.get(
            #interface = getattr(self, '_interface', None),
            grob = getattr(self, '_grob', None),
            attribute = getattr(self, '_attribute', None),
            value = getattr(self, '_vallue', None))
         if matches:
            return matches[0]

   def _right(self, component):
      return [ ]

   def _remove(self, i = None, j = None):
      if i is not None and j is None:
         #self._removeByReference(self[i])
         self._removeByReference(self.components[i])
      elif i is not None and j is not None:
         #for leaf in self[i : j + 1]:
         #   self._removeByReference(leaf)
         for component in self.components[i : j + 1]:
            self._removeByReference(component)
      else:
         #for leaf in self[ : ]:
         #   self._removeByReference(leaf)
         for component in self.components[ : ]:
            self._removeByReference(component)

   #def _removeByReference(self, leaf):
   #   self._components.remove(leaf)
   def _removeByReference(self, component):
      self._components.remove(component)

   def _sever(self, i = None, j = None):
      if i is not None and j is None:
         #leaf = self[i]
         #self._severByReference(leaf)
         component = self.components[i]
         self._severByReference(component)
      elif i is not None and j is not None:
         for n in reversed(range(i, j + 1)):
            #leaf = self[n]
            #self._severByReference(leaf)
            component = self.components[n]
            self._severByReference(component)
      else:
         #for n in reversed(range(len(self))):
         #   leaf = self[n]
         #   self._severByReference(leaf)
         for n in reversed(range(len(self.components))):
            component = self.components[n]
            self._severByReference(component)

   #def _severByReference(self, leaf):
   #   self._blockByReference(leaf)
   #   self._removeByReference(leaf)
   def _severByReference(self, component):
      self._blockByReference(component)
      self._removeByReference(component)

   def _unblock(self, i = None, j = None):
      if i is not None and j is None:
         #leaf = self[i]
         #self._unblockByReference(leaf)
         component = self.components[i]
         self._unblockByReference(component)
      elif i is not None and j is not None:
         #for leaf in self[i : j + 1]:
         #   self._unblockByReference(leaf)
         for component in self.components[i : j + 1]:
            self._unblockByReference(component)
      else:
         #for leaf in self:
         #   self._unblockByReference(leaf)
         for component in self.components:
            self._unblockByReference(component)

   #def _unblockByReference(self, leaf):
   #   if self not in leaf.spanners:
   #      leaf.spanners._append(self)
   def _unblockByReference(self, component):
      if self not in component.spanners._spanners:
         component.spanners._append(self)

   ### PUBLIC ATTRIBUTES ###
   
   @property
   def components(self):
      return self._components[ : ]

   @property
   def duration(self):
      return sum([l.duration.prolated for l in self])

   @property
   def leaves(self):
      result = [ ]
      for component in self._components:
         for node in component._navigator._DFS(forbid = 'Parallel'):
            if node.kind('_Leaf'):
               result.append(node)
      return result

   ### PUBLIC METHODS ###

   def capture(self, n):
      if n > 0:
         cur = self[-1]
         for i in range(n):
            if cur.next:
               self._append(cur.next)
               cur = cur.next         
            else:
               break
      elif n < 0:
         cur = self[0]
         for i in range(abs(n)):
            if cur.prev:
               self._insert(0, cur.prev)
               cur = cur.prev
            else:
               break

   def copy(self, start = None, stop = None):
      result = python_copy(self)
      #result._leaves = [ ]
      result._components = [ ]
      if stop is not None:
         #for leaf in self[start : stop + 1]:
         #   result._leaves.append(leaf)
         for component in self.components[start : stop + 1]:
            result._components.append(component)
      else:
         #for leaf in self:
         #   result._leaves.append(leaf)
         for component in self.components:
            result._components.append(component)
      result._unblock( )
      return result

   def die(self):
      self._sever( )

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
         self._block( )
         return self, left, center, right
      else:
         raise ValueError(
            'direction %s must be left, right or both.' % direction)

   def fuse(self, direction = 'both'):
      if direction == 'left':
         return self._fuseLeft( )
      elif direction == 'right':
         return self._fuseRight( )
      elif direction == 'both':
         result = [ ]
         result.append(self._fuseLeft( ))
         result.append(self._fuseRight( ))
         return result
      else:
         raise ValueError(
            'direction %s must be left, right or both.' % direction)
      
   def index(self, component):
      return self._components.index(component)

   def move(self, n):
      '''
      Move right positive n;
      move left for negative n;
      always preserve length of self.
      '''
      start, stop = self[0], self[-1]
      if n > 0:
         for i in range(n):
            if stop.next:
               self.capture(1)
               self.surrender(-1)
               start, stop = start.next, stop.next
            else:
               break
      elif n < 0:
         for i in range(abs(n)):
            if start.prev:
               self.capture(-1)
               self.surrender(1)      
               start, stop = start.prev, stop.prev
            else:
               break

   def surrender(self, n):
      '''
      Surrender from the right for positive n;
      surrender from the left for negative n;
      never surrender all references;
      (surrender never equals death).
      '''
      if n > 0:
         for i in range(n):
            if len(self) > 1:
               self._sever(-1)
      elif n < 0:
         for i in range(abs(n)):
            if len(self) > 1:
               self._sever(0)
