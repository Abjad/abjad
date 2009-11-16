from abjad.note import Note
from abjad.rational import Rational
from abjad.tools import durtools
from abjad.tools import listtools


def quarter_notes_with_multipliers(pitches, multipliers):
   r'''.. versionadded:: 1.1.2

   Construct list of quarter notes with `multipliers`. ::

      abjad> construct.quarter_notes_with_multipliers([0, 2, 4, 5], [(1, 4), (1, 5), (1, 6), (1, 7)])
      [Note(c', 4 * 1), Note(d', 4 * 5/4), Note(e', 4 * 3/2), Note(f', 4 * 7/4)]

   Read `pitches` cyclically where the length of `pitches` is 
   less than the length of `multipliers`. ::

      abjad> construct.quarter_notes_with_multipliers([0], [(1, 4), (1, 5), (1, 6), (1, 7)])
      [Note(c', 4 * 1), Note(c', 4 * 5/4), Note(c', 4 * 3/2), Note(c', 4 * 7/4)]

   Read `multipliers` cyclically where the length of `multipliers` is
   less than the length of `pitches`. ::

      abjad> construct.quarter_notes_with_multipliers([0, 2, 4, 5], [(1, 5)])
      [Note(c', 4 * 5/4), Note(d', 4 * 5/4), Note(e', 4 * 5/4), Note(f', 4 * 5/4)]
   '''

   quarter_notes = [ ]

   for pitch, multiplier in listtools.zip_cyclic(pitches, multipliers):
      quarter_note = Note(pitch, Rational(1, 4))
      duration_token = durtools.token_unpack(multiplier)
      multiplier = Rational(*duration_token)
      multiplier = Rational(1, 4) / multiplier
      quarter_note.duration.multiplier = multiplier
      quarter_notes.append(quarter_note)

   return quarter_notes
