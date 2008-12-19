from abjad.container.brackets import _Brackets
from abjad.container.duration import _ContainerDurationInterface
from abjad.container.formatter import _ContainerFormatter
from abjad.container.spanner.aggregator import _ContainerSpannerAggregator
from abjad.core.component import _Component
from abjad.helpers.coalesce import coalesce
from abjad.helpers.contiguity import _are_atomic_music_elements
from abjad.helpers.contiguity import _are_contiguous_music_elements
from abjad.helpers.instances import instances
from abjad.helpers.remove_empty_containers import _remove_empty_containers


### TODO - take away the ability to iterate t.spanners and replace
###        with explicit t.spanners.mine, t.spanners.above,
###        t.spanners.below, t.spanners.total read-only properties.

class Container(_Component):

   def __init__(self, music = None):
      music = music or [ ]
      assert isinstance(music, list)
      self._parent = None
      if music:
         music_parent = music[0]._parent
         if not _are_atomic_music_elements(music):
            assert _are_contiguous_music_elements(music)
            start_index = music_parent.index(music[0])
            stop_index = music_parent.index(music[-1])
         if music_parent is not None:
            music_parent[start_index : stop_index + 1] = [self]
      self._music = music
      self._establish( )
      _Component.__init__(self)
      #self._beam = _BeamInterfaceContainer(self)
      self._brackets = _Brackets( )
      self._duration = _ContainerDurationInterface(self)
      self.formatter = _ContainerFormatter(self)
      self.spanners = _ContainerSpannerAggregator(self)

   ### PRIVATE ATTRIBUTES ###

   def _die(self):
      '''
      These two steps work even for nested tuplets.
      '''
      self.spanners.fracture( )
      self._parentage._detach( )

   def _establish(self):
      for x in self._music:
         x._parent = self

#   def _fuseRight(self):
#      '''Fuse self with next container if next is threadable with self.'''
#      next = self._navigator._nextThread
#      if next:
#      ### no need to copy here!
##         self.extend(next.copy( ))
##         next._die( )
#         self.extend(next)
#         next._die( )
#         return 1
#      else:
#         #print 'Nothing to fuse...'
#         return 0

   @property
   def _summary(self):
      if len(self) > 0:
         return ', '.join([str(x) for x in self._music])
      else:
         return ' '

   ### OVERLOADS ###

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
         self._music[i]._die( )
      # slice deletion
      else:
         for m in self._music[i]:
            m._die( )

   ### TODO should we make this non recursive to distinguish it from get( )
   ###      and to make the behaviour more list-like?
   def __getitem__(self, expr):
      if isinstance(expr, str):
         class Visitor(object):
            def __init__(self, name):
               self.name = name
               self.result = None
            def visit(self, node):
               ### this guy will return only the last node with name == self.name. 
               ### What if there are multiple nodes with the same name? Should it return a list?
               if hasattr(node, 'name') and \
                  node.name == self.name:
                  self.result = node
         v = Visitor(expr)
         self._navigator._traverse(v)
         return v.result
      else:
         return self._music[expr]
            
   def __iadd__(self, expr):
      ### iadd avoids unnecessary copying of structures.
      return coalesce([self, expr.copy( )])

   def __imul__(self, n):
      assert isinstance(n, int)
      assert n >= 0
      if n == 0:
         ### TODO - implement this to return empty self.
         ###
         ### This doesn't work:
         ###
         ###   self._music == [ ]
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
         expr._parent = self
         self._music[j] = expr
         if expr.leaves:
            left, right = expr.leaves[0], expr.leaves[-1]
         else:
            left = right = None
      # slice assignment
      else:
         assert isinstance(expr, list)
         for x in expr:
            x._parent = self
         self._music[i.start : i.stop] = expr
         if expr[0].leaves:
            left = expr[0].leaves[0]
         else:
            left = None
         if expr[-1].leaves:
            right = expr[-1].leaves[-1]
         else:
            right = None
      if left and left.prev:
         left.prev.spanners.fracture(direction = 'right')
      if right and right.next:
         right.next.spanners.fracture(direction = 'left')

   ### PUBLIC ATTRIBUTES ###

#   @apply
#   def beam( ):
#      def fget(self):
#         return self._beam
#      return property(**locals( ))

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
      return instances(self, '_Leaf')

   @property
   def next(self):
      '''Next leaf righwards, otherwise None.'''
      if len(self.leaves) > 0:
         return self.leaves[-1].next
      else:
         return None

   ### TODO make this settable?
   @property
   def parallel(self):
      return self.brackets == 'double-angle'

   #### TODO: i propose this instead. 
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

   ### PUBLIC METHODS ### 

   def append(self, expr):
      self.insert(len(self), expr)

#   def coalesce(self): 
#      '''Fuse all sub-containers in self that follow a thread.'''
#      class Visitor(object):
#         def __init__(self):
#            self.merged = False
#         def visit(self, node):
#            if hasname(node, 'Container'):
#               success = node._fuseRight()
#               if success:
#                  self.merged = True
#      v = Visitor( )
#      self._navigator._traverse(v, depthFirst=False, leftRight=False)
#      _remove_empty_containers(self)
#      return v.merged
                  
   def embed(self, i, expr):
      '''
      Non-fracturing insert.
      Insert but *don't* fracture spanners.
      For fracturing insert, use insert( ).
      '''
      def _embedComponent(self, i, expr):
         target = self[i]
         for s in target.spanners:
            for l in expr.leaves:
               s._insert(s.index(target.leaves[0]), l)
         expr._parent = self
         self._music.insert(i, expr)

      if isinstance(expr, (list, tuple)):
         for e in reversed(expr):
            _embedComponent(self, i, e)
      elif isinstance(expr, _Component):
         _embedComponent(self, i, expr)
      else:
         raise TypeError("Can only embed _Component or list of _Component")

   def extend(self, expr):
      if len(expr) > 0:
         if isinstance(expr, list):
            self[len(self) : len(self)] = expr
         elif isinstance(expr, Container):
            self[len(self) : len(self)] = expr[ : ]
         else:
            raise ValueError('Extend containers with lists and containers only.')

   def get(self, name = None, classtype = None):
      '''Searches structure recursively for Components with name <name> 
         and/or class name <classtype>.
         The name may be either an added attribute 
         (e.g. Component.name = 'name') or, in the case of Contexts, 
         the name of the Invocation (e.g. Context.invocation.name = 'name'). '''
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
               elif hasattr(node, 'invocation') and node.invocation.name == self.name:
                  pass
               else:
                  namematch = False
            if self.classtype: 
               if hasattr(node, 'invocation') and node.invocation.type==self.classtype:
                  pass
               elif node.kind(self.classtype):
                  pass
               else:
                  classmatch = False
            if namematch and classmatch:
               self.result.append(node)
      v = Visitor(name, classtype)
      self._navigator._traverse(v)
      return v.result

   def index(self, expr):
      return self._music.index(expr)

   def insert(self, i, expr):
      '''
      Insert and *fracture around* the insert;
      for nonfracturing insert, use embed( ).
      '''
      assert isinstance(expr, _Component)
      result = [ ]
      expr._parent = self
      self._music.insert(i, expr)
      if expr.prev:
         result.extend(expr.prev.spanners.fracture(direction = 'right'))
      if expr.next:
         result.extend(expr.next.spanners.fracture(direction = 'left')) 
      return result

   def pop(self, i = -1):
      result = self[i]
      del(self[i])
      return result

#   def remove(self, i):
#      del(self[i])
   def remove(self, expr):
      class Visitor(object):
         def __init__(self, expr):
            self.expr = expr
            self.deleted = False
         def visit(self, node):
            if node is self.expr:
               node._die( )
               self.deleted = True
      v = Visitor(expr)
      self._navigator._traverse(v)
      if not v.deleted:
         raise ValueError("%s not in list." % expr)
