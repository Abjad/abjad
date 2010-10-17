from abjad.tools.contexttools.ContextMark import ContextMark


class InstrumentMark(ContextMark):
   '''.. versionadded:: 1.1.2

   The Abjad model of an instrument change.
   '''

   _format_slot = 'opening'

   def __init__(self, instrument_name, short_instrument_name, target_context = None):
      from abjad.components import Staff
      from abjad.tools.markuptools import Markup
      ContextMark.__init__(self, target_context = target_context)
      if self.target_context is None:
         self._target_context = Staff
      self._instrument_name = Markup(instrument_name)
      self._short_instrument_name = Markup(short_instrument_name)

   ## OVERLOADS ##

   def __copy__(self, *args):
      return type(self)(self._instrument_name, self._short_instrument_name, 
         target_context = self.target_context)

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         if self.instrument_name == arg.instrument_name:
            if self.short_instrument_name == arg.short_instrument_name:
               return True
      return False

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      result = [ ]
      result.append(r'\set %s.instrumentName = %s' % (self.target_context, self.instrument_name))
      result.append(r'\set %s.shortInstrumentName = %s' % (
         self.target_context, self.short_instrument_name))
      return result

   @property
   def instrument_name(self):
      return self._instrument_name

   @property
   def short_instrument_name(self):
      return self._short_instrument_name
