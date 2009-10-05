from abjad.clef import Clef
from abjad.measure import AnonymousMeasure
from abjad.score import Score
from abjad.staff import Staff
from abjad.staffgroup import PianoStaff
from abjad.tools.chordtools.split_by_pitch_number import \
   split_by_pitch_number as chordtools_split_by_pitch_number
from abjad.tools.io.show import show


def show_chord(chord, template = None, title = None, suppress_pdf = False):
   r""".. versionadded:: 1.1.2

   Split `chord` into treble and bass parts across a temporary
   piano staff and then show the resulting score.

   Return temporary score. ::
   
      abjad> chord = chord = Chord([-29, -21, -18, -15, -11, 10, 12, 14, 20, 23, 28, 29], (1, 4))
      abjad> score = chordtools.show_score(chord)
      abjad> print score.format
      \new Score <<
              \new PianoStaff <<
                      \new Staff {
                              {
                                      \override Staff.TimeSignature #'stencil = ##f
                                      \time 1/4
                                      <bf' c'' d'' af'' b'' e''' f'''>4
                                      \revert Staff.TimeSignature #'stencil
                              }
                      }
                      \new Staff {
                              \clef "bass"
                              {
                                      \override Staff.TimeSignature #'stencil = ##f
                                      \time 1/4
                                      <g,, ef, fs, a, cs>4
                                      \revert Staff.TimeSignature #'stencil
                              }
                      }
              >>
      >>      

   Useful when working with individual chords that have not
   yet been added to score.
   """

   score = Score([ ])
   piano_staff = PianoStaff([ ])
   treble_staff = Staff([ ])
   bass_staff = Staff([ ])
   bass_staff.clef.forced = Clef('bass')
   treble_measure = AnonymousMeasure([ ])
   bass_measure = AnonymousMeasure([ ])

   score.append(piano_staff)
   piano_staff.extend([treble_staff, bass_staff])

   treble_chord, bass_chord = chordtools_split_by_pitch_number(
      chord, pitch = -1)
   
   treble_measure.append(treble_chord)
   bass_measure.append(bass_chord)
   treble_staff.append(treble_measure)
   bass_staff.append(bass_measure)

   show(score, template = template, title = title, suppress_pdf = suppress_pdf)

   return score
