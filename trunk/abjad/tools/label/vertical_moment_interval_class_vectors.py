from abjad.tools import iterate
from abjad.tools import pitchtools


def vertical_moment_interval_class_vectors(expr):
   r'''.. versionadded:: 1.1.2

   Label interval class vector of every vertical moment in `expr`. ::

      abjad> score = Score(Staff([ ]) * 3)
      abjad> score[0].extend(construct.scale(4))
      abjad> score[1].clef.forced = Clef('alto')
      abjad> score[1].extend([Note(-5, (1, 4)), Note(-7, (1, 4))])
      abjad> score[2].clef.forced = Clef('bass')
      abjad> score[2].append(Note(-24, (1, 2)))
      abjad> label.vertical_moment_interval_class_vectors(score)
      abjad> f(score)
      \new Score <<
              \new Staff {
                      c'8
                      d'8 _ \markup { \tiny { 0010020 } }
                      e'8
                      f'8 _ \markup { \tiny { 1000020 } }
              }
              \new Staff {
                      \clef "alto"
                      g4
                      f4 _ \markup { \tiny { 0100110 } }
              }
              \new Staff {
                      \clef "bass"
                      c,2 _ \markup { \tiny { 1000020 } }
              }
      >>
   '''

   for vertical_moment in iterate.vertical_moments_forward_in(expr):
      leaves = vertical_moment.leaves
      pitches = pitchtools.get_pitches(leaves)
      interval_class_vector = pitchtools.get_interval_class_vector(pitches)
      print interval_class_vector
      counts = [ ]
      for i in range(7):
         counts.append(interval_class_vector[i])
      counts = ''.join([str(x) for x in counts])
      counts = r'\tiny { %s }' % counts
      vertical_moment.start_leaves[-1].markup.down.append(counts)
