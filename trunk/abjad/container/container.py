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
#from abjad.helpers.get_dominant_spanners_between import \
#   _get_dominant_spanners_between
from abjad.helpers.get_dominant_spanners_receipt import \
   _get_dominant_spanners_receipt
from abjad.helpers.get_dominant_spanners_slice import \
   _get_dominant_spanners_slice
from abjad.helpers.iterate import iterate
from abjad.helpers.make_orphan_components import _make_orphan_components
from abjad.helpers.remove_empty_containers import _remove_empty_containers
from abjad.helpers.test_components import _test_components
from abjad.notehead.interface import _NoteHeadInterface
from abjad.parentage.parentage import _Parentage


class Container(_Component):

   def __init__(self, music = None):
      music = music or [ ]
      assert isinstance(music, list)
      ## Parentage and spanners must aggregate early.
      ## Reason is so that music can be passed around here
      ## and still respect parentage and spanners.
      self._parentage = _Parentage(self)
      self.spanners = _ContainerSpannerAggregator(self)
      _Component.__init__(self)
      if music:
         parent = music[0].parentage.parent
         if not _are_orphan_components(music):
            _assert_components(music, 'strict', share = 'thread')
            start_index = parent.index(music[0])
            stop_index = parent.index(music[-1])
         if parent is not None:
            parent[start_index : stop_index + 1] = [self]
      self._music = music
      self._establish( )
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
      '''Set expr in self at nonnegative integer index i.
         Give spanners attaching to the current node at i to expr.
         Same with spanners attaching to children of current node at i.
         Operation leaves all score trees always in tact.'''

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
         start, stop, stride = i.indices(len(self))
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
      if len(self) > 0:
         return ', '.join([str(x) for x in self._music])
      else:
         return ' '

   ## PUBLIC ATTRIBUTES ##

   @apply
   def brackets( ):
      def fget(self):
         return self._brackets
      def fset(self, name):
         self._brackets.name = name
      return property(**locals( ))

   @property
   def duration(self):
      return self._duration

   @property
   def leaves(self):
      from abjad.leaf.leaf import _Leaf
      return list(iterate(self, _Leaf))

   @property
   def next(self):
      '''Next leaf righwards, otherwise None.'''
      if len(self.leaves) > 0:
         return self.leaves[-1].next
      else:
         return None

   ## TODO make this settable?
   @property
   def parallel(self):
      return self.brackets in ('double-angle', 'simultaneous')

   ### TODO: i propose this instead. 
   # if we want a next Leaf, we can call a nextLeaf explicitly.
   #   @property
   #   def next(self):
   #      return self._navigator._nextSibling
   @property
   def prev(self):
      '''Prev leaf leftwards, otherwise None.'''
      if len(self.leaves) > 0:
         return self.leaves[0].prev
      else:
         return None

   ## PRIVATE METHODS ##

   ## TODO: Simplify public container methods to use bind ##
   def _bind_component(self, i, component):
      '''Insert component in container music at index i.
         Neither fracture spanners nor insert into spanners.
         With no spanners, this method is the same as insert.
         With spanners, use this method together with spanner insertion.
         Return component.'''
      assert isinstance(component, _Component)
      self._music.insert(i, component)
      #component.parentage.parent = self
      component.parentage._switchParentTo(self)
      self._update._markForUpdateToRoot( )
      return component

   def _establish(self):
      for x in self._music:
         x.parentage.parent = self

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
                  #spanner.insert(spanner.index(self[i]), expr)
                  spanner._insert(spanner.index(self[i]), expr)
         #expr.parentage.parent = self
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
            #self[length:length] = expr[ : ]
            self[length:length] = components
         else:
            raise ValueError(
               'Extend containers with lists and containers only.')
         self._update._markForUpdateToRoot( )

   def index(self, expr):
      '''Return nonnegative index index of expr in self.'''
      return self._music.index(expr)

   def insert(self, i, expr):
      '''Insert and *fracture around* the insert.
         For nonfracturing insert, use embed( ).'''
      assert isinstance(expr, _Component)
      result = [ ]
      #expr.parentage.parent = self
      expr.parentage._switchParentTo(self)
      self._music.insert(i, expr)
      if expr.prev:
         result.extend(expr.prev.spanners.fracture(direction = 'right'))
      if expr.next:
         result.extend(expr.next.spanners.fracture(direction = 'left')) 
      self._update._markForUpdateToRoot( )
      return result

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
