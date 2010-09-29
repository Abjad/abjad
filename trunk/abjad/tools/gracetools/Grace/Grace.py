from abjad.components._Leaf import _Leaf
from abjad.components.Container import Container
from abjad.tools.gracetools.Grace._GraceFormatter import _GraceFormatter


class Grace(Container):
   '''Abjad model of grace music.
   '''

   def __init__(self, music = None, kind = 'grace', **kwargs):
      ## self._carrier is a reference to the Note carrying the Graces.
      self._carrier = None
      Container.__init__(self, music)
      self._formatter = _GraceFormatter(self)
      #self.kind = 'grace'
      self.kind = kind
      self._initialize_keyword_values(**kwargs)

   ## OVERLOADS ##

   def __call__(self, arg):
      if not isinstance(arg, _Leaf):
         raise TypeError('object to which grace attaches much be leaf: "%s".' % arg)
      if self.kind == 'after':
         arg._after_grace = self
         arg.after_grace = self
      else:
         arg._grace = self
         arg.grace = self
      self._carrier = arg
      return arg

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._summary)

   ## PUBLIC ATTRIBUTES ##

   @apply
   def kind( ):
      def fget(self):
         return self._kind
      def fset(self, arg):
         assert arg in ('after', 'grace', 'acciaccatura', 'appoggiatura')
         self._kind = arg
      return property(**locals( ))
