from abjad.components.Note import Note


def label_vertical_moments_in_expr_with_counterpoint_intervals(expr):
   r'''.. versionadded:: 1.1.2

   Label counterpoint interval of every vertical moment in `expr`. ::

      abjad> score = Score(Staff([ ]) * 3)
      abjad> score[0].extend(macros.scale(4))
      abjad> score[1].clef.forced = Clef('alto')
      abjad> score[1].extend([Note(-5, (1, 4)), Note(-7, (1, 4))])
      abjad> score[2].clef.forced = Clef('bass')
      abjad> score[2].append(Note(-24, (1, 2)))
      abjad> verticalitytools.label_vertical_moments_in_expr_with_counterpoint_intervals(score)
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

   .. versionchanged:: 1.1.2
      renamed ``label.vertical_moment_counterpoint_intervals( )`` to
      ``verticalitytools.label_vertical_moments_in_expr_with_counterpoint_intervals( )``.
   '''
   from abjad.tools import iterate
   from abjad.tools import pitchtools

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
         diatonic_interval = pitchtools.calculate_melodic_diatonic_interval_from_named_pitch_to_named_pitch(
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
