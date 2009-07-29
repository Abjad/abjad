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
      '''Read-only tuple of components in spanner. ::

         abjad> voice = Voice(construct.scale(4))
         abjad> spanner = Spanner(voice[:2])
         abjad> spanner.components
         (Note(c', 8), Note(d', 8))

      .. versionchanged:: 1.1.1
         Now returns an immutable tuple instead of a mutable list.
      '''
      return tuple(self._components[:])

   @property
   def duration(self):
      '''Read-only reference to the duration interface serving 
      this spanner. ::

         abjad> voice = Voice(construct.scale(4))
         abjad> spanner = Spanner(voice[:2])
         abjad> spanner.duration
         <_SpannerDurationInterface>

      The spanner duration interface collects use information about the
      duration of the spanner and the components it governs. ::

         abjad> spanner.duration.written
         Rational(1, 4)

      See 
      :class:`~abjad.spanner.duration.interface._SpannerDurationInterface`
      for the complete list of properties and methods available.
      '''

      return self._duration
   
   @property
   def format(self):
      r'''Read-only reference to the spanner format interface that
      serves this spanner. Because the base 
      :class:`~abjad.spanner.spanner.Spanner` class has no graphic
      reality, only concrete classes that inherit from 
      :class:`~abjad.spanner.spanner.Spanner`, 
      such as :class:`~abjad.beam.spanner.Beam` and
      :class:`~abjad.slur.spanner.Slur`, implement this property. ::
      
         abjad> voice = Voice(construct.scale(4))
         abjad> slur = Slur(voice[:]2)
         abjad> slur.format
         <_SlurSpannerFormatInterface>

      See the class documentation for
      :class:`~abjad.slur.spanner.format.interface._SlurSpannerFormatInterface`,
      :class:`~abjad.beam.spanner.format.interface._BeamSpannerFormatInterface`,      and so on for the complete list of properties and methods available.

      .. note:: The spanner ``format`` property differs from the 
         read-only ``format`` property attached to notes, rests, chords,
         measures, voices and other Abjad components.
         The spanner ``format`` property described here returns a
         read-only reference to spanner format interface serving this
         spanner.
         The ``format`` property attached to notes, rests and so on
         returns a string of valid LilyPond input.

      ::

         abjad> spanner.format
         <_SlurSpannerFormatInterface>

         abjad> print voice.format
         \new Voice {
                 c'8 (
                 d'8 )
                 e'8
                 f'8
         }
      '''
      
      return self._format

   @property
   def leaves(self):
      '''Read-only tuple of leaves in spanner. ::

         abjad> voice = Voice(construct.scale(4))
         abjad> spanner = Spanner(voice[:2])
         abjad> spanner.leaves
         (Note(c', 8), Note(d', 8))

      .. versionchanged:: 1.1.1
         Now returns an immutable tuple instead of a mutable list.
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
      '''Read-only reference to the
      :class:`~abjad.spanner.offset._SpannerOffsetInterface` serving
      this spanner. ::

         abjad> voice = Voice(construct.scale(4))
         abjad> spanner = Spanner(voice[:2])
         abjad> spanner.offset
         <_SpannerOffsetInterface>

      Use the spanner offset interface to inspect start- and stop-times
      of this spanner. ::

         abjad> spanner.offset.start
         Rational(0, 1)

      ::

         abjad> spanner.offset.stop
         Rational(1, 4)

      See :class:`~abjad.spanner.offset._SpannerOffsetInterface` for
      details.
      '''
         
      return self._offset

   ## PUBLIC METHODS ##

   def append(self, component):
      '''Add `component` to the right end of `spanner`.

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
      '''Add `component` to the left end of `spanner`.

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

         abjad> staff = Staff(construct.scale(4))
         abjad> beam = Beam(t[:])
         abjad> beam
         Beam(c'8, d'8, e'8, f'8)
         abjad> print staff.format
         \new Staff {
                 c'8 [
                 d'8
                 e'8
                 f'8 ]
         }

      ::
      
         abjad> beam.clear( )
         abjad> beam
         Beam( )
         abjad> len(beam)
         0
         abjad> print staff.format
         \new Staff {
                 c'8
                 d'8
                 e'8
                 f'8
         }
      '''
      self._severAllComponents( )

   def copy(self, start = None, stop = None):
      '''Copy spanner components.

      .. todo:: Deprecate inelegant start / stop interface in 
         Spanner.copy( ) and pass explicit slice instead.
      '''
      my_components = self._components[:]
      self._components = [ ]
      result = python_deepcopy(self)
      self._components = my_components
      if stop is not None:
         for component in self[start : stop + 1]:
            result._components.append(component)
      else:
         for component in self:
            result._components.append(component)
      result._unblockAllComponents( )
      return result

   def extend(self, components):
      from abjad.tools import check
      input = self[-1:]
      input.extend(components)
      check.assert_components(input, contiguity = 'thread')
      for component in components:
         self.append(component)

   def extend_left(self, components):
      from abjad.tools import check
      input = components + self[:1]
      check.assert_components(input, contiguity = 'thread')
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
