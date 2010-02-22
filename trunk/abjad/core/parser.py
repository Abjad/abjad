from abjad.core.abjadcore import _Abjad
#from abjad.scm import Color
#from abjad.scm import Function
from abjad.scm import Moment
from abjad.tools import schemetools


class _Parser(_Abjad):
   '''Utility class to format Abjad values as LilyPond-style Scheme.'''

   ## PRIVATE METHODS ##

   def _isConstant(self, value):
      '''True is ``value`` is constant, otherwise False.'''
      if isinstance(value, int) or isinstance(value, float) or \
          value in ['up', 'down', 'left', 'center', 'right',
         'black', 'white', 'red', 'green',
         'blue', 'cyan', 'magenta', 'yellow',
         'grey', 'darkred', 'darkgreen', 'darkblue',
         'darkcyan', 'darkmagenta', 'darkyellow', ]:
         return True
      else:
         return False

   def _isLilyFunctionName(self, arg):
      '''True if `arg` contains ``::``, otherwise False.'''
      return isinstance(arg, str) and '::' in arg

   ## PUBLIC METHODS ##

   def formatAttribute(self, attribute):
      '''Return Scheme-formatted attribute.'''
      attribute = attribute.replace('__', " #'")
      result = attribute.replace('_', '-')
      result = "#'%s" % result
      return result

   def formatValue(self, value):
      '''Return Scheme-formatted value.'''
      if value is True:
         return '##t'
      elif value is False:
         return '##f'
      elif self._isConstant(value):
         return '#%s' % value
      elif self._isLilyFunctionName(value):
         return '#%s' % value
      elif isinstance(value, (Moment,
         schemetools.SchemeColor, schemetools.SchemeFunction)):
         return '#%s' % value.format
      elif isinstance(value, tuple):
         return "#'(%s . %s)" % value
      elif value.__class__.__name__ in ['Markup']:
         return value.format
      else:
         return "#'%s" % value
