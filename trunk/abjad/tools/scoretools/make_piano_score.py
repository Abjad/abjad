from abjad.measure import AnonymousMeasure
from abjad.score import Score
from abjad.tools.scoretools.make_piano_staff import make_piano_staff
from abjad.tools.chordtools.divide_chord_by_pitch_number import divide_chord_by_pitch_number


def make_piano_score(leaves):
   r""".. versionadded:: 1.1.2

   Create a two-staff, treble / bass score of `leaves`. ::

      abjad> notes = [Note(x, (1, 4)) for x in [-12, 37, -10, 2, 4, 17]]
      abjad> score, treble_staff, bass_staff = scoretools.make_piano_score(notes)
      abjad> f(score)
      \new Score <<
              \new PianoStaff <<
                      \context Staff = "treble" {
                              \clef "treble"
                              r4
                              cs''''4
                              r4
                              ef'''4
                              e'4
                              f''4
                      }
                      \context Staff = "bass" {
                              \clef "bass"
                              c4
                              r4
                              d4
                              r4
                              r4
                              r4
                      }
              >>
      >>
   """

   score, treble_staff, bass_staff = make_piano_staff( )
   for leaf in leaves:
      treble_chord, bass_chord = divide_chord_by_pitch_number(leaf, -1)
      treble_staff.append(treble_chord)
      bass_staff.append(bass_chord)

   return score, treble_staff, bass_staff
