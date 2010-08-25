from abjad.tools.marktools.Mark import Mark
from abjad.tools.markuptools import Markup


class InstrumentMark(Mark):
   '''.. versionadded:: 1.1.2

   Instrument name mark.
   '''

   _format_slot = 'opening'

   def __init__(self, instrument_name, short_instrument_name):
      Mark.__init__(self)
      self.instrument_name = Markup(instrument_name)
      self.short_instrument_name = Markup(short_instrument_name)

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      result = [ ]
      context = self.context.name
      if context is None:
         context = self.context.__class__.__name__
      result.append(r'\set %s.instrumentName = %s' % (context, self.instrument_name))
      result.append(r'\set %s.shortInstrumentName = %s' % (context, self.short_instrument_name))
      return result
