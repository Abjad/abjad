from abjad.note import Note
from abjad.rational import Rational
from abjad.tools import durtools
from abjad.tools import listtools


def quarter_notes_with_multipliers(pitches, durations):
   r'''.. versionadded:: 1.1.2

   Construct list of `quarter_notes` with LilyPond multipliers
   such that ``quarter_notes[i].duration.multiplied`` equals
   ``durations[i]`` for ``i <= len(quarter_notes)``. ::

      abjad> construct.quarter_notes_with_multipliers([0, 2, 4, 5], [(1, 4), (1, 5), (1, 6), (1, 7)])
      [Note(c', 4 * 1), Note(d', 4 * 4/5), Note(e', 4 * 2/3), Note(f', 4 * 4/7)]

   Read `pitches` cyclically where the length of `pitches` is 
   less than the length of `multipliers`. ::

      abjad> construct.quarter_notes_with_multipliers([0], [(1, 4), (1, 5), (1, 6), (1, 7)])
      [Note(c', 4 * 1), Note(c', 4 * 4/5), Note(c', 4 * 2/3), Note(c', 4 * 4/7)]

   Read `multipliers` cyclically where the length of `multipliers` is
   less than the length of `pitches`. ::

      abjad> construct.quarter_notes_with_multipliers([0, 2, 4, 5], [(1, 5)])
      [Note(c', 4 * 4/5), Note(d', 4 * 4/5), Note(e', 4 * 4/5), Note(f', 4 * 4/5)]
   '''

   quarter_notes = [ ]

   for pitch, duration in listtools.zip_cyclic(pitches, durations):
      quarter_note = Note(pitch, Rational(1, 4))
      duration_token = durtools.token_unpack(duration)
      duration = Rational(*duration_token)
      multiplier = duration / Rational(1, 4)
      quarter_note.duration.multiplier = multiplier
      quarter_notes.append(quarter_note)

   return quarter_notes
