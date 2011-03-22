from abjad.tools.contexttools.get_effective_context_mark import get_effective_context_mark
from abjad.tools.contexttools.InstrumentMark import InstrumentMark


def get_effective_instrument(component):
   r'''.. versionadded:: 1.1.2

   Get effective instrument of `component`::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")
      abjad> contexttools.InstrumentMark('Flute', 'Fl.')(staff)
      InstrumentMark('Flute', 'Fl.')

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

   ::

      abjad> for note in staff:
      ...     print note, contexttools.get_effective_instrument(note)
      ... 
      c'8 InstrumentMark('Flute', 'Fl.')
      d'8 InstrumentMark('Flute', 'Fl.')
      e'8 InstrumentMark('Flute', 'Fl.')
      f'8 InstrumentMark('Flute', 'Fl.')

   Return instrument mark or none.
   '''

   return get_effective_context_mark(component, InstrumentMark)
