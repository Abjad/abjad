from abjad.core.abjadcore import _Abjad
from abjad.spanner.duration import _SpannerDurationInterface
from abjad.spanner.format import _SpannerFormatInterface
from abjad.spanner.offset import _SpannerOffsetInterface
from abjad.rational import Rational
from copy import deepcopy as python_deepcopy


class Spanner(_Abjad):
   '''Any type of notation object that stretches horizontally
   and encompasses some number of notes, rest, chords, tuplets,
   measures, voices or other Abjad components. 

   Beams, slurs, hairpins, trills, glissandi and piano pedal brackets
   all stretch horizontally on the page to encompass multiple notes
   and all implement as Abjad spanners.
   That is, these spanner all have an obvious graphic reality with
   definite start-, stop- and midpoints.

   Abjad also implements a number of spanners of a different type,
   such as tempo and instrument spanners, which mark a group of notes,
   rests, chords or measues as carrying a certain tempo or being
   played by a certain instrument.

   The :class:`~abjad.spanner.spanner.Spanner` class described here
   abstracts the functionality that all such spanners, both graphic
   and nongraphics, share. 
   This shared functionality includes methods to add, remove, inspect
   and test components governed by the spanner, as well as basic
   formatting properties.
   The other spanner classes, such as :class:`~abjad.beam.spanner.Beam`
   and :class:`~abjad.glissando.spanner.Glissando`, all inherit from
   this class and receive the functionality implemented here.
   '''

   def __init__(self, music = None):
      '''Apply spanner to music. Init dedicated duration interface.'''
      self._components = [ ]
      self._contiguity_constraint = 'thread'
      self._duration = _SpannerDurationInterface(self)
      self._format = _SpannerFormatInterface(self)
      self._offset = _SpannerOffsetInterface(self)
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

   def _blockAllComponents(self):
      for component in self:
         self._blockComponent(component)

   def _blockComponent(self, component):
      component.spanners._spanners.remove(self)
   
   def _durationOffsetInMe(self, leaf):
      leaves = list(self.leaves)
      assert leaf in leaves
      prev = leaves[:leaves.index(leaf)]
      return sum([leaf.duration.prolated for leaf in prev])

   def _fractureLeft(self, i):
      ##left = self.copy(0, i - 1)
      #left = self.copy(self[:i])
      left = self._copy(self[:i])
      ##right = self.copy(i, len(self))
      #right = self.copy(self[i:])
      right = self._copy(self[i:])
      self._blockAllComponents( )
      return self, left, right

   def _fractureRight(self, i):
      ##left = self.copy(0, i)
      #left = self.copy(self[:i+1])
      left = self._copy(self[:i+1])
      ##right = self.copy(i + 1, len(self))
      #right = self.copy(self[i+1:])
      right = self._copy(self[i+1:])
      self._blockAllComponents( )
      return self, left, right

   def _fuseByReference(self, spanner):
      ##result = self.copy( )
      #result = self.copy(self[:])
      result = self._copy(self[:])
      result.extend(spanner.components)
      self._blockAllComponents( )
      spanner._blockAllComponents( )
      return [(self, spanner, result)]
  
   def _initializeMusic(self, music):
      from abjad.component.component import _Component
      from abjad.leaf.leaf import _Leaf
      from abjad.tools import check
      from abjad.tools import iterate
      music = music or [ ]
      if isinstance(music, _Component):
         music = [music]
      ## TODO: Author staff-level contiguity check in tools/check. ##
      ##       Include optional staff-level contiguity check here. ##
      if self._contiguity_constraint == 'thread':
         leaves = list(iterate.naive(music, _Leaf))
         check.assert_components(leaves, contiguity = 'thread')
      self.extend(music)

   def _insert(self, i, component):
      '''Insert component in spanner at index i.
         Not composer-safe and may mangle spanners.'''
      component.spanners._add(self)
      self._components.insert(i, component)
   
   def _isExteriorLeaf(self, leaf):
      '''True if leaf is first or last in spanner.
      True leaf.next or leaf.prev is None.
      False otherwise.

      .. todo:: Write Spanner._isExteriorLeaf( ) tests.
      '''
      if self._isMyFirstLeaf(leaf):
         return True
      elif self._isMyLastLeaf(leaf):
         return True
      elif not leaf.prev or not leaf.next:
         return True
      else:
         return False

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
         leaves = list(self.leaves)
         i = leaves.index(leaf)
         for x in leaves[:i]:
            if isinstance(x, klass):
               return False
         return True
      return False

   def _isMyLast(self, leaf, klass):
      if isinstance(leaf, klass):
         leaves = list(self.leaves)
         i = leaves.index(leaf)
         for x in leaves[i + 1 : ]:
            if isinstance(x, klass):
               return False
         return True
      return False

   def _isMyOnly(self, leaf, klass):
      return isinstance(leaf, klass) and len(self.leaves) == 1

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
   def components(self):
      '''Return read-only tuple of components in spanner. ::

         abjad> voice = Voice(construct.scale(4))
         abjad> spanner = Spanner(voice[:2])
         abjad> spanner.components
         (Note(c', 8), Note(d', 8))

      .. versionchanged:: 1.1.1
         Now returns an (immutable) tuple instead of a (mutable) list.
      '''
      return tuple(self._components[:])

   @property
   def duration(self):
      '''Return read-only reference to spanner duration interface.
      
      Spanner duration interface implements ``written``, 
      ``preprolated`` and ``prolated`` attributes. ::

         abjad> voice = Voice(construct.scale(4))
         abjad> spanner = Spanner(voice[:2])
         abjad> spanner
         Spanner(c'8, d'8, e'8, f'8)

      ::

         abjad> spanner.duration.written
         Rational(1, 2)

      ::

         abjad> spanner.duration.preprolated
         Rational(1, 2)

      ::

         abjad> spanner.duration.prolated
         Rational(1, 2)

      Spanner duration interface also implements ``seconds`` attribute. ::

         abjad> Tempo(voice[:], TempoIndication(Rational(1, 8), 48))
         abjad> spanner.duration.seconds
         Rational(5, 1)
      '''

      return self._duration
   
#   @property
#   def format(self):
#      '''Return read-only reference to spanner format interface.
#
#      .. todo:: Remove from public interface.
#      '''
#      
#      return self._format

   @property
   def leaves(self):
      '''Return read-only tuple of leaves in spanner. ::

         abjad> voice = Voice(construct.scale(4))
         abjad> spanner = Spanner(voice[:2])
         abjad> spanner.leaves
         (Note(c', 8), Note(d', 8))

      .. versionchanged:: 1.1.1
         Now returns an (immutable) tuple instead of a (mutable) list.
      '''

      from abjad.leaf.leaf import _Leaf
      result = [ ]
      for component in self._components:
         ## EXPERIMENTAL: expand to allow staff-level spanner eventually ##
         #for node in component._navigator._DFS(forbid = 'parallel'):
         for node in component._navigator._DFS( ):
            if isinstance(node, _Leaf):
               result.append(node)
      result = tuple(result)
      return result

   @property
   def offset(self):
      '''.. versionadded:: 1.1.1

      Return read-only reference to spanner offset interface.

      Spanner offset interface implements ``start`` and ``stop`` attributes. ::

         abjad> voice = Voice(construct.scale(4))
         abjad> spanner = Spanner(voice[2:])
         abjad> spanner
         Spanner(e'8, f'8)

      ::

         abjad> spanner.offset.start
         Rational(1, 4)

      ::

         abjad> spanner.offset.stop
         Rational(1, 2)
      '''
         
      return self._offset

   ## PUBLIC METHODS ##

   def append(self, component):
      '''Add `component` to right of spanner.

      :: 

         abjad> voice = Voice(construct.scale(4))
         abjad> spanner = Spanner(voice[:2])
         abjad> spanner
         Spanner(c'8, d'8)

      ::

         abjad> spanner.append(voice[2])
         abjad> spanner
         Spanner(c'8, d'8, e'8)
      '''

      if self._contiguity_constraint == 'thread':
         from abjad.tools import check
         components = self[-1:] + [component]
         check.assert_components(components, contiguity = 'thread')
      component.spanners._add(self)
      self._components.append(component)

   def append_left(self, component):
      '''Add `component` to left of spanner.

      :: 

         abjad> voice = Voice(construct.scale(4))
         abjad> spanner = Spanner(voice[2:])
         abjad> spanner
         Spanner(e'8, f'8)

      ::

         abjad> spanner.append_left(voice[1])
         abjad> spanner
         Spanner(d'8, e'8, f'8)
      '''

      from abjad.tools import check
      components = [component] + self[:1] 
      check.assert_components(components, contiguity = 'thread')
      component.spanners._add(self)
      self._components.insert(0, component)

   def clear(self):
      r'''Remove all components from spanner. ::

         abjad> voice = Voice(construct.scale(4))
         abjad> spanner = Spanner(voice[:])
         abjad> spanner
         Spanner(c'8, d'8, e'8, f'8)

      ::

         abjad> spanner.clear( )
         abjad> spanner
         Spanner( )
      '''

      self._severAllComponents( )

   ##def copy(self, start = None, stop = None):
   #def copy(self, components):
   def _copy(self, components):
      '''Return copy of spanner with `components`.
   
      `components` must be an iterable of components already
      contained in spanner.
      '''

      my_components = self._components[:]
      self._components = [ ]
      result = python_deepcopy(self)
      self._components = my_components

##      if stop is not None:
##         for component in self[start : stop + 1]:
##            result._components.append(component)
##      else:
##         for component in self:
##            result._components.append(component)

      for component in components:
         assert component in self
      for component in components:
         result._components.append(component)
      
      result._unblockAllComponents( )
      return result

   def extend(self, components):
      '''Add iterable `components` to right of spanner. ::

         abjad> voice = Voice(construct.scale(4))
         abjad> spanner = Spanner(voice([:2])
         abjad> spanner
         Spanner(c'8, d'8)

      ::

         abjad> spanner.extend(voice[2:])
         abjad> spanner
         Spanner(c'8, d'8, e'8, f'8)
      '''

      from abjad.tools import check
      input = self[-1:]
      input.extend(components)
      check.assert_components(input, contiguity = 'thread')
      for component in components:
         self.append(component)

   def extend_left(self, components):
      '''Add iterable `components` to left of spanner. ::

         abjad> voice = Voice(construct.scale(4))
         abjad> spanner = Spanner(voice([2:])
         abjad> spanner
         Spanner(e'8, f'8)

      ::

         abjad> spanner.extend_left(voice[:2])
         abjad> spanner
         Spanner(c'8, d'8, e'8, f'8)
      '''

      from abjad.tools import check
      input = components + self[:1]
      check.assert_components(input, contiguity = 'thread')
      for component in reversed(components):
         self.append_left(component)

   def fracture(self, i, direction = 'both'):
      r'''Fracture spanner at `direction` of component at index `i`. 

      Valid values for `direction` are ``'left'``, ``'right'`` and ``'both'``.

      Return original, left and right spanners. ::

         abjad> voice = Voice(construct.scale(4))
         abjad> beam = Beam(voice[:])
         abjad> beam
         Beam(c'8, d'8, e'8, f'8)

      ::

         abjad> beam.fracture(1, direction = 'left')
         (Beam(c'8, d'8, e'8, f'8), Beam(c'8), Beam(d'8, e'8, f'8))

      ::

         abjad> print voice.format
         \new Voice {
                 c'8 [ ]
                 d'8 [
                 e'8
                 f'8 ]
         }
      '''

      if i < 0:
         i = len(self) + i
      if direction == 'left':
         return self._fractureLeft(i)
      elif direction == 'right':
         return self._fractureRight(i)
      elif direction == 'both':
         ##left = self.copy(0, i - 1)
         #left = self.copy(self[:i])
         left = self._copy(self[:i])
         ##right = self.copy(i + 1, len(self))
         #right = self.copy(self[i+1:])
         right = self._copy(self[i+1:])
         ##center = self.copy(i, i)
         #center = self.copy(self[i:i+1])
         center = self._copy(self[i:i+1])
         self._blockAllComponents( )
         return self, left, center, right
      else:
         raise ValueError(
            'direction %s must be left, right or both.' % direction)

   def fuse(self, spanner):
      r'''Fuse contiguous spanners.

      Return new spanner. ::

         abjad> voice = Voice(construct.scale(4))
         abjad> left_beam = Beam(t[:2])
         abjad> right_beam = Beam(t[2:])

      ::

         abjad> print voice.format
         \new Voice {
                 c'8 [
                 d'8 ]
                 e'8 [
                 f'8 ]
         }

      ::
         
         abjad> left_beam.fuse(right_beam)
         [(Beam(c'8, d'8), Beam(e'8, f'8), Beam(c'8, d'8, e'8, f'8))]

      ::

         abjad> print voice.format 
         \new Voice {
                 c'8 [
                 d'8
                 e'8
                 f'8 ]
         }
      
      .. todo:: Return (immutable) tuple instead of (mutable) list.
      '''

      return self._fuseByReference(spanner)
      
   def index(self, component):
      '''Return nonnegative integer index of `component` in spanner. ::

         abjad> voice = Voice(construct.scale(4))
         abjad> spanner = Spanner(voice[2:])
         abjad> spanner
         Spanner(e'8, f'8)

      ::

         abjad> spanner.index(t[-2])
         0
      '''

      return self._components.index(component)

   def pop(self):
      '''Remove and return rightmost component in spanner. ::

         abjad> voice = Voice(construct.scale(4))
         abjad> spanner = Spanner(voice[:])
         abjad> spanner
         Spanner(c'8, d'8, e'8, f'8)

      ::

         abjad> spanner.pop( )
         f'8

      ::

         abjad> spanner
         Spanner(c'8, d'8, e'8)
      '''

      component = self[-1]
      self._severComponent(component)
      return component

   def pop_left(self):
      '''Remove and return leftmost component in spanner. ::

         abjad> voice = Voice(construct.scale(4))
         abjad> spanner = Spanner(voice[:])
         abjad> spanner
         Spanner(c'8, d'8, e'8, f'8)

      ::

         abjad> spanner.pop_left( )
         c'8

      ::

         abjad> spanner
         Spanner(d'8, e'8, f'8)
      '''

      component = self[0]
      self._severComponent(component)
      return component

#   def trim(self, component):
#      assert component in self
#      result = [ ]
#      while not result[:1] == [component]:
#         result.insert(0, self.pop( ))
#      return result 
#
#   def trim_left(self, component):
#      assert component in self
#      result = [ ]
#      while not result[-1:] == [component]:
#         result.append(self.pop( ))
#      return result 
