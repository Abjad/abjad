from abjad.tools.contexttools.ContextMark import ContextMark


class InstrumentMark(ContextMark):
   r'''.. versionadded:: 1.1.2

   The Abjad model of an instrument change::

      abjad> staff = Staff(macros.scale(4))
   
   ::

      abjad> contexttools.InstrumentMark('Flute', 'Fl.')(staff)
      InstrumentMark('Flute', 'Fl.')(Staff{4})

   ::

      abjad> f(staff)
      \new Staff {
         \set Staff.instrumentName = \markup { Flute }
         \set Staff.shortInstrumentName = \markup { Fl. }
         c'8
         d'8
         e'8
         f'8
      }
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

   def __repr__(self):
      markups = (self.instrument_name, self.short_instrument_name)
      contents_string = ', '.join([repr(markup._contents_string) for markup in markups])
      return '%s(%s)' % (self.__class__.__name__, contents_string)

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

   ## PRIVATE ATTRIBUTES ##

   ## will probably need to change definition at some point ##
   @property
   def _target_context_name(self):
      return self.target_context.__name__

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      '''LilyPond input format of instrument mark.
      '''
      result = [ ]
      result.append(r'\set %s.instrumentName = %s' % (
         self._target_context_name, self.instrument_name))
      result.append(r'\set %s.shortInstrumentName = %s' % (
         self._target_context_name, self.short_instrument_name))
      return result

   @property
   def instrument_name(self):
      '''Full name of instrument.
      '''
      return self._instrument_name

   @property
   def short_instrument_name(self):
      '''Short name of instrument.
      '''
      return self._short_instrument_name
