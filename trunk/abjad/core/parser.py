from abjad.core.abjadcore import _Abjad
from abjad.scm.function import Function


class _Parser(_Abjad):

   ## PRIVATE METHODS ##

   def _isConstant(self, value):
      if isinstance(value, int) or isinstance(value, float) or \
          value in ['up', 'down', 'center', 
         'red', 'blue', 'green', 'black', 'white']:
         return True
      else:
         return False

   def _isLilyFunctionName(self, arg):
      return isinstance(arg, str) and '::' in arg

   ## PUBLIC METHODS ##

   def formatAttribute(self, attribute):
      attribute = attribute.replace('__', " #'")
      result = attribute.replace('_', '-')
      result = "#'%s" % result
      return result

   def formatValue(self, value):
      if value is True:
         return '##t'
      elif value is False:
         return '##f'
      elif self._isConstant(value):
         return '#%s' % value
      elif self._isLilyFunctionName(value):
         return '#%s' % value
      elif isinstance(value, Function):
         return '#%s' % value.format
      elif isinstance(value, tuple):
         return "#'(%s . %s)" % value
      ## TODO: The String class does not seem to exist. 
      ##       What to do with it? Remove, create?
      #elif value.__class__.__name__ in ['String', '_Markup']:
      elif value.__class__.__name__ in ['String', 'Markup']:
         return value.format
      else:
         return "#'%s" % value
