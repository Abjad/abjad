from abjad.component.component import _Component
from abjad.container.brackets import _Brackets
from abjad.container.duration import _ContainerDurationInterface
from abjad.container.formatter import _ContainerFormatter
from abjad.container.spanner.aggregator import _ContainerSpannerAggregator
from abjad.debug.debug import debug
from abjad.helpers.are_orphan_components import _are_orphan_components
from abjad.helpers.assert_components import _assert_components
from abjad.helpers.bequeath_multiple import bequeath_multiple
from abjad.helpers.components_detach_parentage import \
   components_detach_parentage
from abjad.helpers.coalesce import coalesce
from abjad.helpers.components_switch_parent_to import \
   _components_switch_parent_to
from abjad.helpers.get_parent_and_index import _get_parent_and_index
from abjad.helpers.get_dominant_spanners_receipt import \
   _get_dominant_spanners_receipt
from abjad.helpers.get_dominant_spanners_slice import \
   _get_dominant_spanners_slice
from abjad.helpers.give_my_attached_spanners_to import \
   _give_my_attached_spanners_to
from abjad.helpers.give_my_position_in_parent_to import \
   _give_my_position_in_parent_to
from abjad.helpers.give_my_spanned_music_to import _give_my_spanned_music_to
from abjad.helpers.iterate import iterate
from abjad.helpers.make_orphan_components import _make_orphan_components
from abjad.helpers.remove_empty_containers import _remove_empty_containers
from abjad.helpers.test_components import _test_components
from abjad.helpers.withdraw_from_crossing_spanners import \
   _withdraw_from_crossing_spanners
from abjad.notehead.interface import _NoteHeadInterface


class Container(_Component):

   def __init__(self, music = None):
      '''Initialize container with music list of length zero or grater.'''
      _Component.__init__(self)
      self.spanners = _ContainerSpannerAggregator(self)
      self._initializeMusic(music)
      self._brackets = _Brackets( )
      self._duration = _ContainerDurationInterface(self)
      self.formatter = _ContainerFormatter(self)
      #self.notehead = _NoteHeadInterface(self)

   ## OVERLOADS ##

   def __add__(self, expr):
      '''Concatenate containers self and expr.
         The operation c = a + b returns a new Container c with
         the content of both a and b.
         The operation is non-commutative: the content of the first
         operand will be placed before the content of the second operand.'''
      return coalesce([self.copy( ), expr.copy( )])

   def __contains__(self, expr):
      '''True if expr is in container, otherwise False.'''
      return expr in self._music

   def __delitem__(self, i):
      '''Remove component at index i in container from container.
         Remove comopnent at index i in container from spanners.
         Return None.'''
      if isinstance(i, int):
         self[i].detach( )
      elif isinstance(i, slice):
         for m in self[i]:
            m.detach( )

   def __getitem__(self, i):
      '''Return component at index i in container.
         Shallow traversal of container for numeric indices only..
         For deep, recursive traversal of container for named indices,
         use Container.get(expr).'''
      return self._music[i]
            
   def __iadd__(self, expr):
      '''__iadd__ avoids unnecessary copying of structures.'''
      return coalesce([self, expr.copy( )])

   def __imul__(self, total):
      '''Multiply contents of container 'total' times.
         Return multiplied container.'''
      from abjad.helpers.contents_multiply import contents_multiply
      return contents_multiply(self, total = total)

   def __len__(self):
      '''Return nonnegative integer number of components in container.'''
      return len(self._music)

   def __radd__(self, expr):
      '''Extend container by contents of expr to the right.'''
      return self + expr

   def __repr__(self):
      '''String format of container for interpreter display.'''
      return '(%s)' % self._summary

   def __setitem__(self, i, expr):
      '''Set 'expr' in self at nonnegative integer index i.
         Or, set 'expr' in self at slice i.
         Find spanners that dominate self[i] and children of self[i].
         Replace contents at self[i] with 'expr'.
         Reattach spanners to new contents.
         This operation leaves all score trees always in tact.'''
      # item assignment
      if isinstance(i, int):
         if not isinstance(expr, _Component):
            raise TypeError('Must be Abjad component.')
         old = self[i]
         spanners_receipt = _get_dominant_spanners_receipt([old])
         ## must withdraw from spanners before parentage!
         ## otherwise begin / end assessments don't work!
         _withdraw_from_crossing_spanners([expr])
         expr.parentage._switchParentTo(self)
         self._music.insert(i, expr)
         detach_receipt = old.detach( )
         for spanner, index in spanners_receipt:
            spanner._insert(index, expr)
            expr.spanners._add(spanner)
      # slice assignment
      else:
         if not _test_components(expr):
            raise TypeError('Must be list of Abjad components.')
         if i.start == i.stop and i.start is not None \
            and i.stop is not None and i.start <= -len(self):
            start, stop = 0, 0
         else:
            start, stop, stride = i.indices(len(self))
         old = self[start:stop]
         spanners_receipt = _get_dominant_spanners_slice(self, start, stop)
         for component in old:
            component.detach( )
         ## must withdraw before setting in self!
         ## otherwise circular withdraw ensues!
         _withdraw_from_crossing_spanners(expr)
         self._music[start:start] = expr
         for component in expr:
            component.parentage._switchParentTo(self)
         for spanner, index in spanners_receipt:
            for component in reversed(expr):
               spanner._insert(index, component)
               component.spanners._add(spanner)
      self._update._markForUpdateToRoot( )

   ## PRIVATE ATTRIBUTES ##

   @property
   def _summary(self):
      '''Formatted summary of container contents for repr output.'''
      if len(self) > 0:
         return ', '.join([str(x) for x in self._music])
      else:
         return ' '

   ## PUBLIC ATTRIBUTES ##

   @apply
   def brackets( ):
      '''Read / write parallel or sequential brackets of container.'''
      def fget(self):
         return self._brackets
      def fset(self, name):
         self._brackets.name = name
      return property(**locals( ))

   @property
   def duration(self):
      '''Read-only reference to container duration interface.'''
      return self._duration

   @property
   def leaves(self):
      '''Python list of all leaves in container.'''
      from abjad.leaf.leaf import _Leaf
      return list(iterate(self, _Leaf))

   @apply
   def parallel( ):
      '''Read / write boolean for paralle / sequential containers.'''
      def fget(self):
         return self.brackets in ('double-angle', 'simultaneous')
      def fset(self, arg):
         assert isinstance(arg, bool)
         if arg == True:
            self.brackets = 'simultaneous'
         else:
            self.brackets = 'sequential'
      return property(**locals( ))
              
   ## PRIVATE METHODS ##

   ## TODO: Deprecate _bind_component. ##

   def _bind_component(self, i, component):
      '''Insert component in container music at index i.
         Neither fracture spanners nor insert into spanners.
         With no spanners, this method is the same as insert.
         With spanners, use this method together with spanner insertion.
         Return component.'''
      assert isinstance(component, _Component)
      self._music.insert(i, component)
      component.parentage._switchParentTo(self)
      self._update._markForUpdateToRoot( )
      return component

   def _initializeMusic(self, music):
      music = music or [ ]
      _assert_components(music, 'strict', share = 'thread')
      if music:
         parent = music[0].parentage.parent
         if parent is not None:
            start_index = parent.index(music[0])
            stop_index = parent.index(music[-1])
            #parent[start_index:stop_index+1] = [self]
            parent._music[start_index:stop_index+1] = [self]
            self.parentage._switchParentTo(parent)
      self._music = music
      for component in self._music:
         component.parentage._switchParentTo(self)

   ## PUBLIC METHODS ## 

   def append(self, component):
      '''Append component to the end of container.
         Preserve any spanners attaching to, or contained in, container.
         Attach no new spanners to component.
         Return None.
         This operation leaves all score trees always in tact.'''
      self[len(self):len(self)] = [component]

   def bequeath(self, component):
      '''Give my music to recipient component.
         Give my attached spanners to recipient component.
         Give my position in parent to recipient component.
         After bequeathal, self is an empty unspanned orphan.
         Bequeath swaps out one type of container for another.
         Return None.''' 
      _give_my_spanned_music_to(self, component)
      _give_my_attached_spanners_to(self, [component])
      _give_my_position_in_parent_to(self, [component])

   def clear(self):
      '''Remove any contents from self.
         Contents have parent set to None.
         Leave all spanners untouched.'''
      result = self._music[ : ]
      for element in result:
         element.parentage._switchParentTo(None)
      self._update._markForUpdateToRoot( )
      return result

   def extend(self, expr):
      '''Extend container with expr.
         Spanners attaching to, or contained in, container remain unchanged.
         No new spanners attach to expr.
         Return None.'''
      if len(expr) > 0:
         if isinstance(expr, list):
            length = len(self)
            self[length:length] = expr
         elif isinstance(expr, Container):
            components = expr[:]
            components = components_detach_parentage(components) 
            length = len(self)
            self[length:length] = components
         else:
            raise TypeError(
               'Must be container or list of Abjad components.')
         self._update._markForUpdateToRoot( )

   def index(self, expr):
      '''Return nonnegative index index of expr in self.'''
      return self._music.index(expr)

   def insert(self, i, component):
      '''Insert component 'component' at index 'i' in container.
         Keep spanners in tact.
         This operation always leaves all Abjad expressions in tact.
         Note that Container.insert( ) previously fracture spanners.'''
      self[i:i] = [component]

   def pop(self, i = -1):
      '''Remove and return element at index i in self.'''
      result = self[i]
      del(self[i])
      return result

   def remove(self, expr):
      '''Remove expr from my music.'''
      class Visitor(object):
         def __init__(self, expr):
            self.expr = expr
            self.deleted = False
         def visit(self, node):
            if node is self.expr:
               node.detach( )
               self.deleted = True
      v = Visitor(expr)
      self._navigator._traverse(v)
      if not v.deleted:
         raise ValueError("%s not in list." % expr)
