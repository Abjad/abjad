from abjad.core.abjadcore import _Abjad


### NOTE: rename _Invocation to _ContextSpecification to better
###       mirror LilyPond's ContextSpeccedMusic class

### NOTE: we used to think of an invocation as a string like
###
###         '\context Voice = "foo" {'
###
###       which included the open curly brace at the end. Note that
###       we're now simplying invocation to equal only something like
###
###         '\context Voice = "foo"'
###
###       without the open curly brace at the end.
###       This makes formatting container \with-blocks cleaner.

### NOTE: command \new or \context is now determined on the fly
###       as a read-only property dependent on the 'name'.

class _Invocation(_Abjad):

   #def __init__(self, client, type = None, name = None, modifications = [ ]):
   def __init__(self, client, type = None, name = None):
      self._client = client
      #self.command = 'new'
      self.name = name
      self.type = type
      #self.modifications = [ ]
      #self.modifications.extend(modifications)

   ### OVERLOADS ###

   def __eq__(self, arg):
      if isinstance(arg, _Invocation):
         #if self.command == arg.command and \
         if self.name == arg.name and \
            self.type == arg.type:
            #self.modifications == arg.modifications:
            return True
         else:
            return False
      return False
         
   def __ne__(self, arg):
      return not self.__eq__(arg)

#   def __repr__(self):
#      result = [ ]
#      if self.type:
#         result.append(self.type)
#      if self.name:
#         result.append(self.name)
#      if self.modifications:
#         result.append(self.modifications)
#      result = [str(x) for x in result]
#      if len(result) > 0:
#         return '_Invocation(%s)' % ', '.join(result)
#      else:
#         return '_Invocation( )'

   ### PRIVATE ATTRIBUTES ###

#   @property
#   def _closing(self):
#      result = [ ]
#      result.append(self._client.brackets.close)
#      return result
#
#   @property
#   def _opening(self):
#      result = [ ]
#      if self.type:
#         cur = '%s %s' % (self.command, self.type)
#         if self.name:
#            cur += ' = "%s"' % self.name
##         if len(self.modifications) > 0:
##            cur += r' \with {'
##            result.append(cur)
##            result.extend(['\t' + x for x in self.modifications])
##            result.append('} %s' % self._client.brackets.open)
##         else:
##            cur += ' %s' % self._client.brackets.open
##            result.append(cur)
#         cur += ' %s' % self._client.brackets.open
#         result.append(cur)
#      else:
#         result.append(self._client.brackets.open)
#      return result

   @property
   def _invocation(self):
      if self.type:
         result = '%s %s' % (self.command, self.type)
         if self.name:
            result += ' = "%s"' % self.name
         return result

   ### PUBLIC ATTRIBUTES ###

#   @apply
#   def command( ):
#      def fget(self):
#         return self._command
#      def fset(self, arg):
#         if isinstance(arg, str):
#            if arg in ('new', 'context'):
#               self._command = '\\' + arg
#            else:
#               raise ValueError('set invocation to "new" or "context" only')
#         else:
#            raise ValueError('set invocation to str only.')
#      return property(**locals( ))

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
         self._name = arg
         #self.command = 'context'
      return property(**locals( ))
