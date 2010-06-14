from abjad.tools import iterate
from abjad.tools import pitchtools


def vertical_moment_pitch_classes(expr):
   r'''.. versionadded:: 1.1.2

   Label pitch classes of every vertical moment in `expr`. ::

      abjad> score = Score(Staff([ ]) * 3)
      abjad> score[0].extend(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> score[1].clef.forced = Clef('alto')
      abjad> score[1].extend([Note(-5, (1, 4)), Note(-7, (1, 4))])
      abjad> score[2].clef.forced = Clef('bass')
      abjad> score[2].append(Note(-24, (1, 2)))
      abjad> label.vertical_moment_pitch_classes(score)
      abjad> f(score)
      \new Score <<
              \new Staff {
                      c'8
                      d'8 _ \markup { \small { \column { 7 2 0 } } }
                      e'8
                      f'8 _ \markup { \small { \column { 5 0 } } }
              }
              \new Staff {
                      \clef "alto"
                      g4
                      f4 _ \markup { \small { \column { 5 4 0 } } }
              }
              \new Staff {
                      \clef "bass"
                      c,2 _ \markup { \small { \column { 7 0 } } }
              }
      >>
   '''

   for vertical_moment in iterate.vertical_moments_forward_in(expr):
      leaves = vertical_moment.leaves
      pitches = pitchtools.get_pitches(leaves)
      if not pitches:
         continue
      pitch_classes = [pitch.pc.number for pitch in pitches]
      pitch_classes = list(set(pitch_classes))
      pitch_classes.sort( )
      pitch_classes.reverse( )
      pitch_classes = ' '.join([str(x) for x in pitch_classes])
      pitch_classes = r'\small { \column { %s } }' % pitch_classes
      vertical_moment.start_leaves[-1].markup.down.append(pitch_classes)
