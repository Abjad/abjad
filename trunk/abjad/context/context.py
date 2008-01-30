from .. containers.container import Container
from formatter import _ContextFormatter
from invocation import _Invocation

class Context(Container):

   def __init__(self, music = [ ]):
      Container.__init__(self, music)
      self.brackets = 'curly'
      self.formatter = _ContextFormatter(self)

   def __repr__(self):
      if len(self) > 0:
         summary = str(len(self))
      else:
         summary = ' '
      return '%s%s%s%s' % (
         self.invocation.lhs,
         self.brackets.open,
         summary,
         self.brackets.close)

   ### MANAGED ATTRIBUTES ###

   @apply
   def invocation( ):
      def fget(self):
         return self._invocation
      def fset(self, arg):
         if arg is None:
            self._invocation = _Invocation(self)
         elif isinstance(arg, str):
            self._invocation = _Invocation(self, lhs = arg)
         elif isinstance(arg, tuple):
            self._invocation = _Invocation(self, *arg)
         else:
            raise ValueError('set invocation to None, str or tuple only.')
      return property(**locals( ))
