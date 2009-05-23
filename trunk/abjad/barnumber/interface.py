from abjad.core.settinghandler import _ContextSettingHandler
from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
import types


class _BarNumberInterface(_Interface, _GrobHandler, _ContextSettingHandler):
   '''Manage *LilyPond* ``BarNumber`` grob.
      Manage *LilyPond* ``currentBarNumber`` context setting.'''

   def __init__(self, _client):
      '''Bind to client and set current bar number to 1.'''
      _Interface.__init__(self, _client)
      _GrobHandler.__init__(self, 'BarNumber')
      self.current = None

   ## PUBLIC ATTRIBUTES ##

   @apply
   def current( ):
      '''Read / write *LilyPond* ``currentBarNumber`` context setting.'''
      def fget(self):
         return self._current
      def fset(self, expr):
         assert isinstance(expr, (int, types.NoneType))
         self._current = expr
      return property(**locals( ))

   ## TODO: Abstract formatting stuff to _ContextSettingHandler. ##

   @property
   def settings(self):
      '''List of *LilyPond* context settings.'''
      result = [ ]
      if self.current is not None:
         formatted_value = self._parser.formatValue(self.current)
         context = getattr(self._client, 'context', None)
         if context is not None:
            result.append(r'currentBarNumber = %s' %
               formatted_value)
         else:
            promotion = self._promotions.get('current', None)
            if promotion is not None:
               result.append(r'\set %s.currentBarNumber = %s' % (
                  promotion, formatted_value))
            else:
               result.append(r'\set currentBarNumber = %s' %
                  formatted_value)
      return result
