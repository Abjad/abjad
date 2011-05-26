from fractions import Fraction
from abjad.components import Score
from abjad.components import Staff
from abjad.tools import componenttools
from abjad.tools import contexttools
from abjad.tools import schemetools
from abjad.tools.tonalitytools.make_first_n_notes_in_ascending_diatonic_scale import make_first_n_notes_in_ascending_diatonic_scale



def make_all_notes_in_ascending_and_descending_diatonic_scale(key_signature = None):
   r'''.. versionadded:: 1.1.2

   Construct one up-down period of scale according to `key_signature`::

      abjad> score = macros.scale_period(contexttools.KeySignatureMark('E', 'major'))
      abjad> f(score)
      \new Score \with {
              tempoWholesPerMinute = #(ly:make-moment 30 1)
      } <<
              \new Staff {
                      \key e \major
                      e'8
                      fs'8
                      gs'8
                      a'8
                      b'8
                      cs''8
                      ds''8
                      e''8
                      ds''8
                      cs''8
                      b'8
                      a'8
                      gs'8
                      fs'8
                      e'4
              }
      >>

   .. versionchanged:: 1.1.2
      renamed ``construct.scale_period( )`` to
      ``tonalitytools.make_all_notes_in_ascending_and_descending_diatonic_scale( )``.

   .. versionchanged:: 1.1.2
      renamed ``leaftools.make_all_notes_in_ascending_and_descending_diatonic_scale( )`` to
      ``tonalitytools.make_all_notes_in_ascending_and_descending_diatonic_scale( )``.
   '''

   ascending_notes = make_first_n_notes_in_ascending_diatonic_scale(
      8, Fraction(1, 8), key_signature)
   descending_notes = componenttools.clone_components_and_remove_all_spanners(ascending_notes[:-1])
   descending_notes.reverse( )
   notes = ascending_notes + descending_notes
   notes[-1].duration.written = Fraction(1, 4)
   staff = Staff(notes)
   contexttools.KeySignatureMark(key_signature.tonic, key_signature.mode)(staff)
   score = Score([staff])
   score.set.tempo_wholes_per_minute = schemetools.SchemeMoment(30)

   return score
