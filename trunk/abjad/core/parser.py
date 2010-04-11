from abjad.core.abjadcore import _Abjad


class _Parser(_Abjad):
   '''Utility class to format Abjad values as LilyPond-style Scheme.'''

   ## PRIVATE METHODS ##

   def _is_constant(self, value):
      '''True if value is constant, otherwise False.'''
      if isinstance(value, int) or isinstance(value, float) or \
          value in ['up', 'down', 'left', 'center', 'right',
         'black', 'white', 'red', 'green',
         'blue', 'cyan', 'magenta', 'yellow',
         'grey', 'darkred', 'darkgreen', 'darkblue',
         'darkcyan', 'darkmagenta', 'darkyellow', ]:
         return True
      else:
         return False

   def _is_lily_function_name(self, arg):
      '''True if arg contains '::', otherwise False.'''
      return isinstance(arg, str) and '::' in arg

   ## PUBLIC METHODS ##

   def format_attribute(self, attribute):
      '''Return Scheme-formatted attribute.'''
      attribute = attribute.replace('__', " #'")
      result = attribute.replace('_', '-')
      result = "#'%s" % result
      return result

   def format_value(self, value):
      '''Return Scheme-formatted value.'''
      if value is True:
         return '##t'
      elif value is False:
         return '##f'
      elif self._is_constant(value):
         return '#%s' % value
      elif self._is_lily_function_name(value):
         return '#%s' % value
      elif isinstance(value, tuple):
         return "#'(%s . %s)" % value
      elif isinstance(value, str):
         return "#'%s" % value
      elif hasattr(value, 'format'):
         return value.format
      else:
         return "#'%s" % value
