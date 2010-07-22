from abjad.note import Note
from abjad.tools import iterate
from abjad.tools import pitchtools


def vertical_moment_counterpoint_intervals(expr):
   r'''.. versionadded:: 1.1.2

   Label counterpoint interval of every vertical moment in `expr`. ::

      abjad> score = Score(Staff([ ]) * 3)
      abjad> score[0].extend(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> score[1].clef.forced = Clef('alto')
      abjad> score[1].extend([Note(-5, (1, 4)), Note(-7, (1, 4))])
      abjad> score[2].clef.forced = Clef('bass')
      abjad> score[2].append(Note(-24, (1, 2)))
      abjad> label.vertical_moment_counterpoint_intervals(score)
      abjad> f(score)
      \new Score <<
              \new Staff {
                      c'8
                      d'8 _ \markup { \small { \column { 2 5 } } }
                      e'8
                      f'8 _ \markup { \small { \column { 4 4 } } }
              }
              \new Staff {
                      \clef "alto"
                      g4
                      f4 _ \markup { \small { \column { 3 4 } } }
              }
              \new Staff {
                      \clef "bass"
                      c,2 _ \markup { \small { \column { 8 5 } } }
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
      melodic_diatonic_intervals = [ ]
      for upper_note in upper_notes:
         diatonic_interval = pitchtools.pitches_to_diatonic_interval(
            bass_note.pitch, upper_note.pitch)
         melodic_diatonic_intervals.append(diatonic_interval)    
      intervals = melodic_diatonic_intervals
      hcpics = [ ]
      for mdi in melodic_diatonic_intervals:
         hcpic = pitchtools.HarmonicCounterpointIntervalClass(mdi)
         hcpics.append(hcpic)
      intervals = ' '.join([str(x) for x in hcpics])
      intervals = r'\small { \column { %s } }' % intervals
      vertical_moment.start_leaves[-1].markup.down.append(intervals)
