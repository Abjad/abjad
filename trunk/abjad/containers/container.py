from brackets import Brackets
from .. core.component import _Component
from formatter import ContainerFormatter
from containerspanner import ContainerSpannerInterface
from .. duration.duration import Duration
from .. note.note import Note

class Container(_Component):

   def __init__(self, music = [ ]):
      self._parent = None
      self._music = music
      self._establish( )
      _Component.__init__(self)
      self._brackets = Brackets( )
      self.formatter = ContainerFormatter(self)
      self.spanners = ContainerSpannerInterface(self)

   ### INIT UTILS ###

   def _establish(self):
      for x in self._music:
         x._parent = self

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
      duration = Duration(0)
      for x in self:
         duration += x.duration
      return duration

   @property
   def duratum(self):
      result = self._parentage._prolation * self.duration
      return Duration(*result.pair)

   ### NAVIGATION ###

   @property
   def next(self):
      '''
      Next leaf righwards, otherwise None.
      '''
      if len(self.leaves) > 0:
         return self.leaves[-1].next
      else:
         return None

   @property
   def prev(self):
      '''
      Prev leaf leftwards, otherwise None.
      '''
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
         #del(self[j])
         #self._music.insert(j, expr)
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
         #del(self[i])
         #self._music[i.start : i.start] = expr
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
         #left.prev.spanners.fractureRight( )
         left.prev.spanners.fracture(direction = 'right')
      if right and right.next:
         #right.next.spanners.fractureLeft( )
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
      other types of insert are possible;
      for example, nonfracturing insert;
      other insert types not yet implemented.
      '''
      assert isinstance(expr, _Component)
      result = [ ]
      expr._parent = self
      self._music.insert(i, expr)
      if expr.prev:
         #result.extend(expr.prev.spanners.fractureRight( ))
         result.extend(expr.prev.spanners.fracture(direction = 'right'))
      if expr.next:
         #result.extend(expr.next.spanners.fractureLeft( )) 
         result.extend(expr.next.spanners.fracture(direction = 'left')) 
      return result

   def append(self, expr):
      self.insert(len(self), expr)

   def extend(self, expr):
      self[len(self) : len(self)] = expr

   def pop(self, i = None):
      if i is None:
         del(self[-1])
      else:
         del(self[i])

   def _killLeaves(self, i = None, j = None):
      '''
      First step in killing a container;
      killing leaves eliminates crossing spanners.
      '''
      if i and j:
         for l in self.leaves[i : j + 1]:
            l._die( )
      else:
         for l in self.leaves:
            l._die( )

   def _die(self):
      '''
      These two steps work even for nested tuplets.
      '''
      self._killLeaves( )   
      self._parentage._detach( )

   ### GETTERS ###

   def getInstances(self, name):
      class Visitor(object):
         def __init__(self, name):
            self.result = []
         def visit(self, node):
            if node.kind(name):
               self.result.append(node)
      v = Visitor(name)
      self._navigator._traverse(v)
      return v.result

   @property
   def leaves(self):
      return self.getInstances('Leaf')

#   ### ORPHANED GETTERS AND SETTERS ###
#
#   def setInitialTempo(self, tempoString):
#      self[0].before.append(
#         r"\override Score.MetronomeMark #'padding = #8")
#      self[0].before.append(
#         r"\override Score.MetronomeMark #'font-size = #3")
#      self[0].before.append(r'\tempo ' + tempoString)
