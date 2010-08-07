from abjad.components.Note import Note
from abjad.tools import iterate
from abjad.tools.tonalitytools.are_scalar_notes import are_scalar_notes
from abjad.tools.tonalitytools.are_stepwise_notes import are_stepwise_notes


def is_neighbor_note(note):
   r'''.. versionadded:: 1.1.2

   True when `note` is preceeded by a stepwise interval in one direction
   and followed by a stepwise interval in the other direction.
   Otherwise false. ::

      abjad> t = Staff(macros.scale(4))
      abjad> for note in t:
      ...     print '%s\t%s' % (note, tonalitytools.is_neighbor_note(note))
      ... 
      c'8     False
      d'8     False
      e'8     False
      f'8     False
   '''
   
   if not isinstance(note, Note):
      raise TypeError('must be note: %s' % note)

   try:
      prev_note = iterate.get_nth_namesake_from_component(note, -1) 
      next_note = iterate.get_nth_namesake_from_component(note, 1)
   except IndexError:
      return False

   notes = [prev_note, note, next_note]

   return are_stepwise_notes(notes) and not are_scalar_notes(notes)
