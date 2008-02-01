from .. helpers.hasname import hasname
from .. barline.interface import _BarLineInterface
from comments import _Comments
from copier import _Copier
from .. core.navigator import _Navigator
from .. core.parentage import _Parentage
from .. duration.rational import Rational
from .. staff.interface import _StaffInterface # This is not being used here?
from .. tempo.interface import _TempoInterface

class _Component(object):

   def __init__(self):
      self._accidentals = None
      self._barline = _BarLineInterface(self)
      self._copier = _Copier(self)
      self.comments = _Comments( )
      self._navigator = _Navigator(self)
      self._parentage = _Parentage(self)
      self._tempo = _TempoInterface(self)

   ### CLASS NAME TESTING ###
   
   def kind(self, classname):
      return hasname(self, classname)

   ### COPY ###

   def __mul__(self, n):
      result = [ ]
      for i in range(n):
         result.append(self.copy( ))
      return result

   def __rmul__(self, n):
      return self * n

   def copy(self, i = None, j = None):
      return self._copier.copy(i, j)

   ### MANAGED ATTRIBUTES ###

   @apply
   def tempo( ):
      def fget(self):
         return self._tempo
      def fset(self, expr):
         if expr is None:
            self._tempo._metronome = None
         elif isinstance(expr, (tuple)):
            assert isinstance(expr, tuple)
            assert isinstance(expr[0], (tuple, Rational))
            assert isinstance(expr[1], (int, float, long))
            from .. note.note import Note
            if isinstance(expr[0], tuple):
               self._tempo._metronome = (Note(0, expr[0]), expr[1])
            elif isinstance(expr[0], Rational):
               self._tempo._metronome = (Note(0, expr[0]), expr[1])
      return property(**locals( ))
            
   @apply
   def barline( ):
      def fget(self):
         return self._barline
      def fset(self, type):
         self._barline.type = type
      return property(**locals( ))

   ### TODO - make work for leaves, too    ###
   ###        add stuff to leaf formatters ###

   @apply
   def accidentals( ):
      def fget(self):
         return self._accidentals
      def fset(self, style):
         assert isinstance(style, (str, type(None)))
         self._accidentals = style
      return property(**locals( ))

   ### PROPERTIES ###

   @property
   def format(self):
      return self.formatter.lily
