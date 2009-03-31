from abjad.core.abjadcore import _Abjad
import types


## NOTE: rename _Invocation to _ContextSpecification to better
##       mirror LilyPond's ContextSpeccedMusic class

## NOTE: we used to think of an invocation as a string like
##
##         '\context Voice = "foo" {'
##
##       which included the open curly brace at the end. Note that
##       we're now simplying invocation to equal only something like
##
##         '\context Voice = "foo"'
##
##       without the open curly brace at the end.
##       This makes formatting container \with-blocks cleaner.

## NOTE: command \new or \context is now determined on the fly
##       as a read-only property dependent on the 'name'.

class _Invocation(_Abjad):

   def __init__(self, client, type = None, name = None):
      self._client = client
      self.name = name
      self.type = type

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, _Invocation):
         if self.name == arg.name and \
            self.type == arg.type:
            return True
         else:
            return False
      return False
         
   def __ne__(self, arg):
      return not self.__eq__(arg)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _invocation(self):
      if self.type:
         result = '%s %s' % (self.command, self.type)
         if self.name:
            result += ' = "%s"' % self.name
         return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def command(self):
      if self.name:
         return r'\context'
      else:
         return r'\new'

   @apply
   def name( ):
      def fget(self):
         return self._name
      def fset(self, arg):
         assert isinstance(arg, (str, types.NoneType))
         self._name = arg
         self._client._name = arg
      return property(**locals( ))
