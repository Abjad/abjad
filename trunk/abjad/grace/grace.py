from .. containers.container import Container
from formatter import _GraceFormatter


class Grace(Container):

   def __init__(self, music = None):
      music = music or None
      Container.__init__(self, music)
      self.formatter = _GraceFormatter(self)
      self.type = 'grace'

   def __repr__(self):
      return 'Grace(%s)' % self._summary

   ### MANAGED ATTRIBUTES ###

   @apply
   def type( ):
      def fget(self):
         return self._type
      def fset(self, arg):
         assert arg in ('after', 'grace', 'acciaccatura', 'appoggiatura')
         self._type = arg
      return property(**locals( ))
