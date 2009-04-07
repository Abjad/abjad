from abjad.container.container import Container
from abjad.grace.formatter import _GraceFormatter


class Grace(Container):

   def __init__(self, music = None):
      ## self._carrier is a reference to the Note carrying the Graces.
      self._carrier = None
      music = music or None
      Container.__init__(self, music)
      self._formatter = _GraceFormatter(self)
      self.kind = 'grace'

   ## OVERLOADS ##

   def __repr__(self):
      return 'Grace(%s)' % self._summary

   ## PUBLIC ATTRIBUTES ##

   @apply
   def kind( ):
      def fget(self):
         return self._kind
      def fset(self, arg):
         assert arg in ('after', 'grace', 'acciaccatura', 'appoggiatura')
         self._kind = arg
      return property(**locals( ))
