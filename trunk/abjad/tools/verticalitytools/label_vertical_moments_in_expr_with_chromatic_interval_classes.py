from abjad.components.Note import Note


def label_vertical_moments_in_expr_with_chromatic_interval_classes(expr):
   r'''.. versionadded:: 1.1.2

   Label harmonic chromatic interval classes 
   of every vertical moment in `expr`. ::

      abjad> score = Score(Staff([ ]) * 3)
      abjad> score[0].extend(macros.scale(4))
      abjad> score[1].clef.forced = Clef('alto')
      abjad> score[1].extend([Note(-5, (1, 4)), Note(-7, (1, 4))])
      abjad> score[2].clef.forced = Clef('bass')
      abjad> score[2].append(Note(-24, (1, 2)))
      abjad> verticalitytools.label_vertical_moments_in_expr_with_chromatic_interval_classes(score)
      abjad> f(score)
      \new Score <<
              \new Staff {
                      c'8
                      d'8 _ \markup { \small { \column { 2 7 } } }
                      e'8
                      f'8 _ \markup { \small { \column { 5 5 } } }
              }
              \new Staff {
                      \clef "alto"
                      g4
                      f4 _ \markup { \small { \column { 4 5 } } }
              }
              \new Staff {
                      \clef "bass"
                      c,2 _ \markup { \small { \column { 0 7 } } }
              }
      >>

   .. versionchanged:: 1.1.2
      renamed ``label.vertical_moment_chromatic_interval_classes( )`` to
      ``verticalitytools.label_vertical_moments_in_expr_with_chromatic_interval_classes( )``.
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
      hcics = [ ]
      for upper_note in upper_notes:
         hcic = pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_to_pitch(
            bass_note, upper_note)
         hcics.append(hcic)
      hcics = ' '.join([str(hcic) for hcic in hcics])
      hcics = r'\small { \column { %s } }' % hcics
      vertical_moment.start_leaves[-1].markup.down.append(hcics)
