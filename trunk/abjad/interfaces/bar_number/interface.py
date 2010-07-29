from abjad.core.settinghandler import _ContextSettingHandler
from abjad.core.grobhandler import _GrobHandler
from abjad.interfaces.interface.interface import _Interface
import types


class BarNumberInterface(_Interface, _GrobHandler, _ContextSettingHandler):
   '''Manage bar number attributes.

      *  Handle LilyPond ``BarNumber`` grob.
      *  Manage LilyPond ``currentBarNumber`` context setting.

      ::

         abjad> t = RigidMeasure((2, 8), macros.scale(2))
         abjad> t.bar_number
         <BarNumberInterface>
   '''

   def __init__(self, _client):
      _Interface.__init__(self, _client)
      _GrobHandler.__init__(self, 'BarNumber')
      self.current = None

   ## PUBLIC ATTRIBUTES ##

   @apply
   def current( ):
      def fget(self):
         '''Read / write LilyPond ``currentBarNumber`` context setting.

         *  Default value: ``None``.
         *  All values: integer, ``None``.         

         :: 

            abjad> t = RigidMeasure((2, 8), macros.scale(2))
            abjad> t[0]
            abjad> t[0].bar_number.current = 22
            abjad> t[0].bar_number.current
            22
         '''
         return self._current
      def fset(self, expr):
         assert isinstance(expr, (int, types.NoneType))
         self._current = expr
      return property(**locals( ))

   ## TODO: Abstract formatting stuff to _ContextSettingHandler. ##

   @property
   def settings(self):
      r'''Read-only list of LilyPond context settings
      picked up at format-time.

      *  Derived from ``BarNumberInterface.current``.

      ::

         abjad> t = RigidMeasure((2, 8), macros.scale(2))
         abjad> t[0]
         abjad> t[0].bar_number.current = 22
         abjad> print t.format
                 \time 2/8
                 \set currentBarNumber = #22
                 c'8
                 d'8
      '''
      result = [ ]
      if self.current is not None:
         formatted_value = self._parser.format_value(self.current)
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
