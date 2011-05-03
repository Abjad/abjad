from abjad.tools import contexttools


def get_effective_instrument(component):
   r'''.. versionadded:: 1.1.2

   Get effective instrument from `component`::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")
      abjad> instrumenttools.Flute( )(staff)
      Flute('Flute', 'Fl.')

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

      abjad> instrumenttools.get_effective_instrument(staff[0])
      Flute('Flute', 'Fl.')

   Return instrument or none.
   '''

   return contexttools.get_effective_instrument(component)
