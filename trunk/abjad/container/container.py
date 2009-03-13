from abjad.component.component import _Component
from abjad.container.brackets import _Brackets
from abjad.container.duration import _ContainerDurationInterface
from abjad.container.formatter import _ContainerFormatter
from abjad.container.spanner.aggregator import _ContainerSpannerAggregator
from abjad.helpers.are_contiguous_components import _are_contiguous_components
from abjad.helpers.are_orphan_components import _are_orphan_components
from abjad.helpers.bequeath_multiple import bequeath_multiple
from abjad.helpers.coalesce import coalesce
from abjad.helpers.get_parent_and_index import _get_parent_and_index
from abjad.helpers.iterate import iterate
from abjad.helpers.remove_empty_containers import _remove_empty_containers
from abjad.notehead.interface import _NoteHeadInterface
from abjad.parentage.parentage import _Parentage


class Container(_Component):

   def __init__(self, music = None):
      music = music or [ ]
      assert isinstance(music, list)
      self._parentage = _Parentage(self)
      _Component.__init__(self)
      if music:
         parent = music[0].parentage.parent
         if not _are_orphan_components(music):
            assert _are_contiguous_components(music)
            start_index = parent.index(music[0])
            stop_index = parent.index(music[-1])
         if parent is not None:
            parent[start_index : stop_index + 1] = [self]
      self._music = music
      self._establish( )
      #_Component.__init__(self)
      self._brackets = _Brackets( )
      self._duration = _ContainerDurationInterface(self)
      self.formatter = _ContainerFormatter(self)
      ## TODO: Reimplement _NoteHeadInterface on _Component
      self.notehead = _NoteHeadInterface(self)
      self.spanners = _ContainerSpannerAggregator(self)

   ## OVERLOADS ##

   def __add__(self, expr):
      '''Concatenate containers self and expr.
      The operation c = a + b returns a new Container c with
      the content of both a and b.
      The operation is non-commutative: the content of the first
      operand will be placed before the content of the second operand.'''
      return coalesce([self.copy( ), expr.copy( )])

   def __contains__(self, expr):
      return expr in self._music

   def __delitem__(self, i):
      # item deletion
      if isinstance(i, int):
         self._music[i].detach( )
      # slice deletion
      else:
         for m in self._music[i]:
            m.detach( )

   ## TODO Should we make __getitem__ non recursive to distinguish 
   ##      it from get( ) and to make the behaviour more list-like?

   def __getitem__(self, expr):
      if isinstance(expr, str):
         class Visitor(object):
            def __init__(self, name):
               self.name = name
               self.result = None
            def visit(self, node):
               ## this guy will return only the last node 
               ## with name == self.name. 
               ## What if there are multiple nodes with the same name? 
               ## Should it return a list?
               if hasattr(node, 'name') and \
                  node.name == self.name:
                  self.result = node
         v = Visitor(expr)
         self._navigator._traverse(v)
         return v.result
      else:
         return self._music[expr]
            
   def __iadd__(self, expr):
      '''__iadd__ avoids unnecessary copying of structures.'''
      return coalesce([self, expr.copy( )])

   def __imul__(self, n):
      assert isinstance(n, int)
      assert n >= 0
      if n == 0:
         ## TODO - implement this to return empty self.
         ##
         ## This doesn't work:
         ##
         ##   self._music == [ ]
         pass
      else:
         for copy in self * (n - 1):
            self.extend(copy)
      return self

   def __len__(self):
      return len(self._music)

   def __radd__(self, expr):
      return self + expr

   def __repr__(self):
      return '(%s)' % self._summary

   def __setitem__(self, i, expr):
      # item assignment
      if isinstance(i, int):
         assert isinstance(expr, _Component)
         if i < 0:
            j = len(self) + i
         else:
            j = i
         expr.parentage._switchParentTo(self)
         self._music[j] = expr

         #if expr.leaves:
         #   left, right = expr.leaves[0], expr.leaves[-1]
         #else:
         #   left = right = None

      # slice assignment
      else:
         assert isinstance(expr, list)
         for x in expr:
            x.parentage._switchParentTo(self)
         self._music[i.start : i.stop] = expr

         #if expr[0].leaves:
         #   left = expr[0].leaves[0]
         #else:
         #   left = None
         #if expr[-1].leaves:
         #   right = expr[-1].leaves[-1]
         #else:
         #   right = None

      #if left and left.prev:
      #   left.prev.spanners.fracture(direction = 'right')
      #if right and right.next:
      #   right.next.spanners.fracture(direction = 'left')

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
      return self.brackets == 'double-angle'

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
      #component.parentage._setParentTo(self)
      component.parentage.parent = self
      return component

   def _establish(self):
      for x in self._music:
         #x.parentage._setParentTo(self)
         x.parentage.parent = self

   ## PUBLIC METHODS ## 

   def append(self, expr):
      '''Append the end of my music.
         Fracture spanners.'''
      self.insert(len(self), expr)

   def bequeath(self, expr):
      '''Experimental: Bequeath my music, my position-in-spanners, and 
         my position-in-parent to empty container expr. 

         After bequeathal, self is an empty unspanned orphan.

         Bequeathal is basically a way of casting one type of container
         to another; bequeathal is also cleaner than (leaf) casting;
         bequeathal leaves all container attributes completely in tact.'''
      assert isinstance(expr, Container)
      assert not len(expr)

      # give my music to expr
      expr.extend(self)
      self._music[ : ] = [ ]

      # for every spanner attached to me ...
      for spanner in list(self.spanners.attached):
         # insert expr in spanner just before me ...
         spanner.insert(spanner.index(self), expr)
         # ... and then remove me from spanner
         spanner.remove(self)

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
                  spanner.insert(spanner.index(self[i]), expr)
         #expr.parentage._setParentTo(self)
         expr.parentage.parent = self
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
            self[len(self) : len(self)] = expr
         elif isinstance(expr, Container):
            self[len(self) : len(self)] = expr[ : ]
         else:
            raise ValueError(
               'Extend containers with lists and containers only.')
         self._update._markForUpdateToRoot( )

   def get(self, name = None, classtype = None):
      '''Searches structure recursively for Components with name <name> 
         and/or class name <classtype>.
         The name may be either an added attribute 
         (e.g. Component.name = 'name') or, in the case of Contexts, 
         the name of the Invocation (e.g. Context.invocation.name = 'name').'''
      class Visitor(object):
         def __init__(self, name = name, classtype = classtype):
            self.classtype = classtype
            self.name = name
            self.result = [ ]
         def visit(self, node):
            namematch = True
            classmatch = True
            if self.name:
               if (hasattr(node, 'name') and self.name == node.name):   
                  pass
               elif hasattr(node, 'invocation') and \
                  node.invocation.name == self.name:
                  pass
               else:
                  namematch = False
            if self.classtype: 
               if hasattr(node, 'invocation') and \
                  node.invocation.type == self.classtype:
                  pass
               elif not isinstance(self.classtype, str) and \
                  isinstance(node, classtype):
                  pass
               else:
                  classmatch = False
            if namematch and classmatch:
               self.result.append(node)
      v = Visitor(name, classtype)
      self._navigator._traverse(v)
      return v.result

   def index(self, expr):
      '''Return nonnegative index index of expr in self.'''
      return self._music.index(expr)

   def insert(self, i, expr):
      '''Insert and *fracture around* the insert.
         For nonfracturing insert, use embed( ).'''
      assert isinstance(expr, _Component)
      result = [ ]
      #expr.parentage._setParentTo(self)
      expr.parentage.parent = self
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

   ## TODO: Externalize to container_slip(container) helper

   def slip(self):
      '''Bequeath my parent and my spanners to my children.
         Return me.'''
      return bequeath_multiple([self], self[:])[0]
