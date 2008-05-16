from abjad.containers.brackets import _Brackets
from abjad.core.component import _Component
from abjad.containers.duration import _ContainerDurationInterface
from abjad.containers.formatter import _ContainerFormatter
from abjad.helpers.contiguity import _are_atomic_music_elements
from abjad.helpers.contiguity import _are_contiguous_music_elements
from abjad.helpers.hasname import hasname
from abjad.helpers.instances import instances
from abjad.containers.spannerinterface import _ContainerSpannerInterface

class Container(_Component):

   def __init__(self, music = [ ]):
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
      self._brackets = _Brackets( )
      self._duration = _ContainerDurationInterface(self)
      self.formatter = _ContainerFormatter(self)
      self.spanners = _ContainerSpannerInterface(self)

   ### INIT UTILS ###

   def _establish(self):
      for x in self._music:
         x._parent = self

   ### SPECIAL OVERRIDES ###

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

   ### REPR ###

   @property
   def _summary(self):
      if len(self) > 0:
         return ', '.join([str(x) for x in self._music])
      else:
         return ' '

   def __repr__(self):
      if len(self) > 0:
         return '(%s)' % self._summary
      else:
         return '( )'

   ### PROPERTIES ###

   def __len__(self):
      return len(self._music)

   @property
   def parallel(self):
      return self.brackets == 'double-angle'

   ### MANAGED ATTRIBUTES ###

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

   ### NAVIGATION ###

   @property
   def next(self):
      '''Next leaf righwards, otherwise None.'''
      if len(self.leaves) > 0:
         return self.leaves[-1].next
      else:
         return None

   @property
   def prev(self):
      '''Prev leaf leftwards, otherwise None.'''
      if len(self.leaves) > 0:
         return self.leaves[0].prev
      else:
         return None

   ### ACCESSORS ###

   def __contains__(self, expr):
      return expr in self._music

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

   def __delitem__(self, i):
      # item deletion
      if isinstance(i, int):
         self._music[i]._die( )
      # slice deletion
      else:
         for m in self._music[i]:
            m._die( )

   ### MUSIC MANAGEMENT ###

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

   def embed(self, i, expr):
      '''
      Non-fracturing insert.
      Insert but *don't* fracture spanners.
      For fracturing insert, use insert( ).
      '''
      def _embedComponent(self, i, expr):
         for l in expr.leaves:
            for s in self.spanners.get():
               s._insert(s.index(self[i].leaves[0]), l)
         expr._parent = self
         self._music.insert(i, expr)

      if isinstance(expr, (list, tuple)):
         for e in reversed(expr):
            _embedComponent(self, i, e)
      elif isinstance(expr, _Component):
         _embedComponent(self, i, expr)
      else:
         raise TypeError("Can only embed _Component or list of _Component")

      
   def append(self, expr):
      self.insert(len(self), expr)

   def extend(self, expr):
      if isinstance(expr, list):
         self[len(self) : len(self)] = expr
      elif isinstance(expr, Container):
         self[len(self) : len(self)] = expr[ : ]
      else:
         raise ValueError('Extend containers with lists and containers only.')

   def pop(self, i = -1):
      result = self[i]
      del(self[i])
      return result

   def remove(self, i):
      del(self[i])

   def _die(self):
      '''
      These two steps work even for nested tuplets.
      '''
      self.spanners.fracture( )
      self._parentage._detach( )

   @property
   def leaves(self):
      return instances(self, '_Leaf')
