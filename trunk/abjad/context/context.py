from abjad.container.container import Container
from abjad.context.formatter import _ContextFormatter
from abjad.context.invocation import _Invocation


class _Context(Container):

   def __init__(self, music = None):
      music = music or [ ]
      Container.__init__(self, music)
      self.brackets = 'curly'
      self.formatter = _ContextFormatter(self)

   def __repr__(self):
      if len(self) > 0:
         summary = str(len(self))
      else:
         summary = ' '
      return '%s%s%s%s' % (
         self.invocation.type,
         self.brackets.open,
         summary,
         self.brackets.close)

   ### TODO: eliminate this in favor of ID-only equivalence,
   ###       just like all the other system components;
   ###       if we want to preserve this functionality,
   ###       either test all three attributes by hand,
   ###       or save this functionality off as a different
   ###       function in the public interface
   def __eq__(self, arg):
      if isinstance(arg, _Context):
         if self.brackets == arg.brackets and \
            self.invocation == arg.invocation and\
            self._music == arg._music:
            return True
         else:
            return False
      return False

   def __ne__(self, arg):
      return not self.__eq__(arg)

   ### MANAGED ATTRIBUTES ###

   @apply
   def invocation( ):
      def fget(self):
         return self._invocation
      def fset(self, arg):
         if arg is None:
            self._invocation = _Invocation(self)
         elif isinstance(arg, str):
            self._invocation = _Invocation(self, type = arg)
         elif isinstance(arg, tuple):
            self._invocation = _Invocation(self, *arg)
         else:
            raise ValueError('set invocation to None, str or tuple only.')
      return property(**locals( ))
