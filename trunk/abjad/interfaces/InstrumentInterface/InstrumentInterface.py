from abjad.core import _GrobHandler
from abjad.core import _ContextSettingHandler
from abjad.interfaces._Interface import _Interface
from abjad.interfaces._SpannerReceptor import _SpannerReceptor
from abjad.marks import Markup
from abjad.spanners import InstrumentSpanner
import types


class InstrumentInterface(_Interface, _GrobHandler, _ContextSettingHandler, 
   _SpannerReceptor):
   r'''Receive Abjad :class:`~abjad.instrument.spanner.InstrumentSpanner`.
   Handle the LilyPond ``InstrumentName`` grob.

   ::

      abjad> t = Staff(macros.scale(4))
      abjad> t.instrument
      <InstrumentInterface>

   ::

      abjad> t.instrument.color = 'red'
      abjad> print t.format
      \new Staff \with {
         \override InstrumentName #'color = #red
      } {
         c'8
         d'8
         e'8
         f'8
      }
   '''

   def __init__(self, client):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'InstrumentName')
      _SpannerReceptor.__init__(self, (InstrumentSpanner, ))
      self._short_name = None
      self._name = None

   ## PUBLIC ATTRIBUTES ##

   @apply
   def name( ):
      def fget(self):
         r'''Read / write LilyPond ``instrumentName`` context setting.

         *  Default value: ``None``.
         *  All values: ``str``, ``Markup``, ``None``.

         ::

            abjad> t = Staff(macros.scale(4))
            abjad> t.instrument.name = 'Violini I'


         ::

            abjad> print t.format
            \new Staff \with {
               instrumentName = "Violini I"
            } {
               c'8
               d'8
               e'8
               f'8
            }
         '''
         return self._name
      def fset(self, expr):
         assert isinstance(expr, (str, Markup, types.NoneType))
         self._name = expr
      return property(**locals( ))

   @property
   def settings(self):
      r'''Read-only list of LilyPond context settings
      picked up at format-time.

      *  Derived from ``name`` and ``short_name``.

      ::

         abjad> t = Staff(macros.scale(4))
         abjad> t.instrument.name = 'Violini I'
         abjad> t.instrument.short_name = 'Vni. I'
         abjad> t.instrument.settings
         ['instrumentName = "Violini I"', 'shortInstrumentName = "Vni. I"']
      '''
      result = [ ]
      name = self.name
      if name is not None:
         if isinstance(name, Markup):
            name_contribution = name.format
         else:
            name_contribution = '"%s"' % name
         result.append('instrumentName = %s' % name_contribution)
      short_name = self.short_name
      if short_name is not None:
         if isinstance(short_name, Markup):
            short_name_contribution = short_name.format
         else:
            short_name_contribution = '"%s"' % short_name
         result.append('shortInstrumentName = %s' % short_name_contribution)
      return result
      
   @apply
   def short_name( ):
      def fget(self):
         r'''Read / write LilyPond ``shortInstrumentName`` context setting.

         *  Default value: ``None``.
         *  All values: ``str``, ``Markup``, ``None``.

         ::

            abjad> t = Staff(macros.scale(4))
            abjad> t.instrument.short_name = 'Vni. I'


         ::

            abjad> print t.format
            \new Staff \with {
               shortInstrumentName = "Vni. I"
            } {
               c'8
               d'8
               e'8
               f'8
            }
         '''
         return self._short_name
      def fset(self, expr):
         assert isinstance(expr, (str, Markup, types.NoneType))
         self._short_name = expr
      return property(**locals( ))
