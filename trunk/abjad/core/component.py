from abjad.barline.interface import _BarLineInterface
from abjad.clef.interface import _ClefInterface
from abjad.core.comments import _Comments
from abjad.core.navigator import _Navigator
from abjad.core.parentage import _Parentage
from abjad.helpers.hasname import hasname
from abjad.rational.rational import Rational
from abjad.tempo.interface import _TempoInterface
from copy import deepcopy


class _Component(object):

   def __init__(self):
      self._accidentals = None
      self._barline = _BarLineInterface(self)
      self._clef = _ClefInterface(self)
      self._comments = _Comments( )
      self._navigator = _Navigator(self)
      self._parentage = _Parentage(self)
      self._tempo = _TempoInterface(self)

   ### OVERLOADS ###

   def __cmp__(self, arg):
      raise Exception(NotImplemented)

   def __eq__(self, arg):
      return id(self) == id(arg)

   def __mul__(self, n):
      result = [ ]
      for i in range(n):
         result.append(self.copy( ))
      return result

   def __ne__(self, arg):
      return id(self) != id(arg)

   def __nonzero__(self):
      return True

   def __rmul__(self, n):
      return self * n

   ### PUBLIC ATTRIBUTES ###

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

   @apply
   def barline( ):
      def fget(self):
         return self._barline
      def fset(self, type):
         self._barline.type = type
      return property(**locals( ))

   @apply
   def clef( ):
      def fget(self):
         return self._clef
      def fset(self, arg):
         self._clef.forced = arg
      return property(**locals( ))

   @apply
   def comments( ):
      def fget(self):
         return self._comments
      def fset(self, type):
         raise AttributeError('can not overwrite _Comments.')
      return property(**locals( ))

   @property
   def format(self):
      return self.formatter.lily

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

   ### PUBLIC METHODS ###

   def copy(self):
      '''
      Clones a complete Abjad object;
      first fractures and then cuts parent;
      (cut followed by fracture destroys 'next');
      deepcopies reference-pruned version of self;
      reestablishes parent and spanner references;
      returns the deepcopy;
      leaves self unchanged.
      '''
      hairpins = self.spanners.get(classname = '_Hairpin')
      hairpinKillList = [ ]
      clientLeaves = set(self.leaves)
      hairpinKillList = [
         not set(hp[ : ]).issubset(clientLeaves) for hp in hairpins]
      receipt = self.spanners.fracture( )
      parent = self._parentage._cutOutgoingReferenceToParent( )
      result = deepcopy(self)
      for source, left, right in reversed(receipt):
         source._unblock( )
         left._sever( )
         right._sever( )
      self._parent = parent
      for i, hp in enumerate(result.spanners.get(classname = '_Hairpin')):
         if hairpinKillList[i]:
            hp.die( )
      return result

   def kind(self, classname):
      return hasname(self, classname)
