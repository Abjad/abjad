from abjad.note import Note
from abjad.tools import iterate
from abjad.tools import pitchtools


def vertical_moment_diatonic_intervals(expr):
   r'''.. versionadded:: 1.1.2

   Label diatonic intervals of every vertical moment in `expr`. ::

      abjad>

   '''

   for vertical_moment in iterate.vertical_moments_forward_in(expr):
      leaves = vertical_moment.leaves
      notes = [leaf for leaf in leaves if isinstance(leaf, Note)]
      notes.sort(lambda x, y: cmp(x.pitch.number, y.pitch.number))
      notes.reverse( )
      bass_note = notes[-1]
      upper_notes = notes[:-1]
      diatonic_intervals = [ ]
      for upper_note in upper_notes:
         pass
         #diatonic_interval = pitchtools.
