from abjad.container import Container
from abjad.context.formatter import _ContextFormatter


class _Context(Container):

   def __init__(self, music = None):
      Container.__init__(self, music)
      self._formatter = _ContextFormatter(self)

   ## OVERLOADS ##

   def __repr__(self):
      '''.. versionchanged:: 1.1.2
         Named contexts now print name at the interpreter.'''
      if len(self) > 0:
         summary = str(len(self))
      else:
         summary = ' '
      if self.parallel:
         open, close = '<<', '>>'
      else:
         open, close = '{', '}'
      name = self.name
      if name is not None:
         name = '-"%s"' % name
      else:
         name = ''
      #return '%s%s%s%s' % (self.context, open, summary, close)
      return '%s%s%s%s%s' % (self.context, name, open, summary, close)

   ## PUBLIC ATTRIBUTES ##

   @apply
   def context( ):
      def fget(self):
         return self._context
      def fset(self, arg):
         assert isinstance(arg, str)
         self._context = arg
      return property(**locals( ))
