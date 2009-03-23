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
from abjad.helpers.get_parent_and_index import _get_parent_and_index
from abjad.helpers.get_dominant_spanners_receipt import \
   _get_dominant_spanners_receipt
from abjad.helpers.get_dominant_spanners_slice import \
   _get_dominant_spanners_slice
from abjad.helpers.iterate import iterate
from abjad.helpers.make_orphan_components import _make_orphan_components
from abjad.helpers.remove_empty_containers import _remove_empty_containers
from abjad.helpers.test_components import _test_components
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
      ## TODO: Reimplement _NoteHeadInterface on _Component
      self.notehead = _NoteHeadInterface(self)

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
         expr.parentage._switchParentTo(self)
         self._music.insert(i, expr)
         detach_receipt = old.detach( )
         for spanner, index in spanners_receipt:
            spanner._insert(index, expr)
            expr.spanners._update([spanner])
      # slice assignment
      else:
         if not _test_components(expr):
            raise TypeError('Must be list of Abjad components.')
         print i, i.start, i.stop
         if i.start == i.stop and i.start is not None \
            and i.stop is not None and i.start <= -len(self):
            start, stop = 0, 0
         else:
            start, stop, stride = i.indices(len(self))
         print start, stop
         old = self[start:stop]
         spanners_receipt = _get_dominant_spanners_slice(self, start, stop)
         for component in old:
            component.detach( )
         self._music[start:start] = expr
         for component in expr:
            component.parentage._switchParentTo(self)
         for spanner, index in spanners_receipt:
            for component in reversed(expr):
               spanner._insert(index, component)
               component.spanners._update([spanner])
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

   @property
   def next(self):
      '''Naive next leaf righwards, otherwise None.'''
      if len(self.leaves) > 0:
         return self.leaves[-1].next
      else:
         return None

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
              
   ### TODO: i propose this instead. 
   # if we want a next Leaf, we can call a nextLeaf explicitly.
   #   @property
   #   def next(self):
   #      return self._navigator._nextSibling

   @property
   def prev(self):
      '''Naive prev leaf leftwards, otherwise None.'''
      if len(self.leaves) > 0:
         return self.leaves[0].prev
      else:
         return None

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
            parent[start_index:stop_index+1] = [self]
      self._music = music
      for component in self._music:
         component.parentage._switchParentTo(self)

   ## PUBLIC METHODS ## 

   def append(self, expr):
      '''Append the end of my music.
         Fracture spanners.'''
      self.insert(len(self), expr)

   def bequeath(self, expr):
      '''Experimental: Bequeath my music, my position-in-spanners, and 
         my position-in-parent to some other Abjad component.

         After bequeathal, self is an empty unspanned orphan.

         Bequeathal is basically a way of casting one type of container
         to another; bequeathal is also cleaner than (leaf) casting;
         bequeathal leaves all container attributes completely in tact.'''

      ## if I have contents, can only bequeath to empty container
      if len(self) > 0:
         assert isinstance(expr, Container)
         assert not len(expr)

         # give my music to expr
         expr.extend(self)
         self._music[ : ] = [ ]

      # for every spanner attached to me ...
      for spanner in list(self.spanners.attached):
         # insert expr in spanner just before me ...
         #spanner.insert(spanner.index(self), expr)
         spanner._components.insert(spanner.index(self), expr)
         expr.spanners._update([spanner])
         # ... and then remove me from spanner
         #spanner.remove(self)
         spanner._severComponent(self)

      # if i have a parent
      parent = self.parentage.parent
      if parent:
         # embed expr in parent just before me ... 
         parent.embed(parent.index(self), expr)
         # .. and then remove me from parent
         parent.remove(self)

   def clear(self):
      '''Remove any contents from self.
         Contents have parent set to None.
         Leave all spanners untouched.'''
      result = self._music[ : ]
      for element in result:
         element.parentage._switchParentTo(None)
      self._update._markForUpdateToRoot( )
      return result

   def embed(self, i, expr):
      '''Insert a _Component or list of _Components 
         in this container at index i 
         without fracturing spanners.'''
      def _embedComponent(self, i, expr):
         if i != 0:
            bounding_spanners = \
               self[i - 1].spanners.attached & self[i].spanners.attached
            if bounding_spanners:
               for spanner in bounding_spanners:
                  spanner._insert(spanner.index(self[i]), expr)
         expr.parentage._switchParentTo(self)
         self._music.insert(i, expr)

      if isinstance(expr, (list, tuple)):
         for e in reversed(expr):
            _embedComponent(self, i, e)
      elif isinstance(expr, _Component):
            _embedComponent(self, i, expr)
      else:
         raise TypeError("Can only embed _Component or list of _Component")
      self._update._markForUpdateToRoot( )

   def extend(self, expr):
      '''Extend my music and fracture spanners.
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
            raise ValueError(
               'Extend containers with lists and containers only.')
         self._update._markForUpdateToRoot( )

   def index(self, expr):
      '''Return nonnegative index index of expr in self.'''
      return self._music.index(expr)

#   def insert(self, i, expr):
#      '''Insert and *fracture around* the insert.
#         For nonfracturing insert, use embed( ).'''
#      assert isinstance(expr, _Component)
#      result = [ ]
#      expr.parentage._switchParentTo(self)
#      self._music.insert(i, expr)
#      if expr.prev:
#         result.extend(expr.prev.spanners.fracture(direction = 'right'))
#      if expr.next:
#         result.extend(expr.next.spanners.fracture(direction = 'left')) 
#      self._update._markForUpdateToRoot( )
#      return result

   def insert(self, i, component):
      '''Insert component 'component' at index 'i' in container.
         Keep spanners in tact.
         This operation always leaves all Abjad expressions in tact.
         Note that Contianer.insert( ) previously fracture spanners.'''
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
