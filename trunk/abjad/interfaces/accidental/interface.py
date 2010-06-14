from abjad.core.settinghandler import _ContextSettingHandler
from abjad.core.grobhandler import _GrobHandler
from abjad.interfaces.interface.interface import _Interface
import types


class AccidentalInterface(_Interface, _GrobHandler, _ContextSettingHandler):
   '''Interface to all accidental-related settings and information.

   * Manage LilyPond Accidental grob.
   * Manage LilyPond ``set-accidental-style`` function.
   * Interface to LilyPond ``suggestAccidentals`` context setting.

   ::

      abjad> t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> t.accidental
      <AccidentalInterface>
   '''

   def __init__(self, _client):
      _Interface.__init__(self, _client)
      _GrobHandler.__init__(self, 'Accidental')
      self.style = None
      self.suggest_accidentals = None

   ## PRIVATE ATTRIBUTES ##

   @property
   def _opening(self):
      '''Format contribution at container opening.'''
      result = [ ]
      style = self.style
      if style:
         result.append(r"#(set-accidental-style '%s)" % style)
      return result

   ## PUBLIC ATTRIBUTES ##

   ## TODO: Abstract formatting stuff to _ContextSettingHandler. ##

   @property
   def settings(self):
      r'''Read-only list of LilyPond context settings picked up
      at format-time.

      * Derived from `suggest_accidentals`.
      '''
      result = [ ]
      if self.suggest_accidentals is not None:
         formatted_value = self._parser.format_value(self.suggest_accidentals)
         context = getattr(self._client, 'context', None)
         if context is not None:
            result.append(r'suggestAccidentals = %s' % formatted_value)
         else:
            promotion = self._promotions.get('suggest_accidentals', None)
            if promotion is not None:
               result.append(r'\set %s.suggestAccidentals = %s' % (
                  promotion, formatted_value))
            else:
               result.append(r'\set suggestAccidentals = %s' %
                  formatted_value)
      return result

   @apply
   def style( ):
      def fget(self):
         r'''Read / write LilyPond accidental style.
      
         *  Default value: ``None``.
         *  All values: LilyPond accidental style string, ``None``.

         ::

            abjad> t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
            abjad> t.accidental.style = 'forget'

         ::

            abjad> print t.format
            \new Staff {
                    #(set-accidental-style 'forget)
                    c'8
                    d'8
                    e'8
                    f'8
            }
         '''
         return self._style
      def fset(self, arg):
         assert isinstance(arg, (str, types.NoneType))
         self._style = arg
      return property(**locals( ))

   @apply
   def suggest_accidentals( ):
      def fget(self):
         r'''Read / write LilyPond ``suggestAccidentals`` context setting.
         '''
         return self._suggest_accidentals
      def fset(self, arg):
         if not isinstance(arg, (bool, types.NoneType)):
            raise TypeError('must be true, false or none.')
         self._suggest_accidentals = arg
      return property(**locals( ))
