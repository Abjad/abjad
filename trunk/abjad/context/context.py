from abjad.container.container import Container
from abjad.context.formatter import _ContextFormatter


class _Context(Container):

   def __init__(self, music = None):
      music = music or [ ]
      Container.__init__(self, music)
      self._formatter = _ContextFormatter(self)

   ## OVERLOADS ##

   def __repr__(self):
      if len(self) > 0:
         summary = str(len(self))
      else:
         summary = ' '
      if self.parallel:
         open, close = '<<', '>>'
      else:
         open, close = '{', '}'
      return '%s%s%s%s' % (self.context, open, summary, close)

   ## PUBLIC ATTRIBUTES ##

   @apply
   def context( ):
      def fget(self):
         return self._context
      def fset(self, arg):
         assert isinstance(arg, str)
         self._context = arg
      return property(**locals( ))
