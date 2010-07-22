from abjad.note import Note
from abjad.tools import iterate
from abjad.tools import pitchtools


def vertical_moment_chromatic_intervals(expr):
   r'''.. versionadded:: 1.1.2

   Label harmonic chromatic intervals 
   of every vertical moment in `expr`. ::

      abjad> score = Score(Staff([ ]) * 3)
      abjad> score[0].extend(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> score[1].clef.forced = Clef('alto')
      abjad> score[1].extend([Note(-5, (1, 4)), Note(-7, (1, 4))])
      abjad> score[2].clef.forced = Clef('bass')
      abjad> score[2].append(Note(-24, (1, 2)))
      abjad> label.vertical_moment_chromatic_intervals(score)
      abjad> f(score)
      \new Score <<
              \new Staff {
                      c'8
                      d'8 _ \markup { \small { \column { 26 19 } } }
                      e'8
                      f'8 _ \markup { \small { \column { 29 17 } } }
              }
              \new Staff {
                      \clef "alto"
                      g4
                      f4 _ \markup { \small { \column { 28 17 } } }
              }
              \new Staff {
                      \clef "bass"
                      c,2 _ \markup { \small { \column { 24 19 } } }
              }
      >>
   '''

   for vertical_moment in iterate.vertical_moments_forward_in_expr(expr):
      leaves = vertical_moment.leaves
      notes = [leaf for leaf in leaves if isinstance(leaf, Note)]
      if not notes:
         continue
      notes.sort(lambda x, y: cmp(x.pitch.number, y.pitch.number))
      notes.reverse( )
      bass_note = notes[-1]
      upper_notes = notes[:-1]
      hcis = [ ]
      for upper_note in upper_notes:
         hci = pitchtools.harmonic_chromatic_interval_from_to(
            bass_note, upper_note)
         hcis.append(hci)
      hcis = ' '.join([str(hci) for hci in hcis])
      hcis = r'\small { \column { %s } }' % hcis
      vertical_moment.start_leaves[-1].markup.down.append(hcis)
