from abjad.tools import listtools


def iterate_named_chromatic_pitch_pairs_forward_in_expr(expr):
   r'''.. versionadded:: 1.1.2

   Iterate left-to-right, top-to-bottom pitch pairs in `expr`. ::

      abjad> score = Score([ ])
      abjad> notes = macros.scale(4) + [Note(7, (1, 4))]
      abjad> score.append(Staff(notes))
      abjad> notes = [Note(x, (1, 4)) for x in [-12, -15, -17]]
      abjad> score.append(Staff(notes))
      abjad> contexttools.ClefMark('bass')(score[1])

   ::

      abjad> f(score)
      \new Score <<
              \new Staff {
                      c'8
                      d'8
                      e'8
                      f'8
                      g'4
              }
              \new Staff {
                      \clef "bass"
                      c4
                      a,4
                      g,4
              }
      >>

   ::

      abjad> for pair in pitchtools.iterate_named_chromatic_pitch_pairs_forward_in_expr(score):
      ...     pair
      ... 
      (NamedPitch(c, 4), NamedPitch(c, 3))
      (NamedPitch(c, 4), NamedPitch(d, 4))
      (NamedPitch(c, 3), NamedPitch(d, 4))
      (NamedPitch(d, 4), NamedPitch(e, 4))
      (NamedPitch(d, 4), NamedPitch(a, 2))
      (NamedPitch(c, 3), NamedPitch(e, 4))
      (NamedPitch(c, 3), NamedPitch(a, 2))
      (NamedPitch(e, 4), NamedPitch(a, 2))
      (NamedPitch(e, 4), NamedPitch(f, 4))
      (NamedPitch(a, 2), NamedPitch(f, 4))
      (NamedPitch(f, 4), NamedPitch(g, 4))
      (NamedPitch(f, 4), NamedPitch(g, 2))
      (NamedPitch(a, 2), NamedPitch(g, 4))
      (NamedPitch(a, 2), NamedPitch(g, 2))
      (NamedPitch(g, 4), NamedPitch(g, 2))

   Chords are handled correctly. ::

      abjad> chord_1 = Chord([0, 2, 4], (1, 4))
      abjad> chord_2 = Chord([17, 19], (1, 4))
      abjad> staff = Staff([chord_1, chord_2])

   ::

      abjad> f(staff)
      \new Staff {
              <c' d' e'>4
              <f'' g''>4
      }

   ::

      abjad> for pair in pitchtools.iterate_named_chromatic_pitch_pairs_forward_in_expr(staff):
      ...   print pair
      (NamedPitch(c, 4), NamedPitch(d, 4))
      (NamedPitch(c, 4), NamedPitch(e, 4))
      (NamedPitch(d, 4), NamedPitch(e, 4))
      (NamedPitch(c, 4), NamedPitch(f, 5))
      (NamedPitch(c, 4), NamedPitch(g, 5))
      (NamedPitch(d, 4), NamedPitch(f, 5))
      (NamedPitch(d, 4), NamedPitch(g, 5))
      (NamedPitch(e, 4), NamedPitch(f, 5))
      (NamedPitch(e, 4), NamedPitch(g, 5))
      (NamedPitch(f, 5), NamedPitch(g, 5))

   .. versionchanged:: 1.1.2
      renamed ``iterate.pitch_pairs_forward_in( )`` to
      ``pitchtools.iterate_named_chromatic_pitch_pairs_forward_in_expr( )``.

   .. versionchanged:: 1.1.2
      renamed ``iterate.pitch_pairs_forward_in_expr( )`` to
      ``pitchtools.iterate_named_chromatic_pitch_pairs_forward_in_expr( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.iterate_pitch_pairs_forward_in_expr( )`` to
      ``pitchtools.iterate_named_chromatic_pitch_pairs_forward_in_expr( )``.
   '''
   from abjad.tools.leaftools.iterate_leaf_pairs_forward_in_expr import iterate_leaf_pairs_forward_in_expr

   from abjad.tools import pitchtools
   for leaf_pair in iterate_leaf_pairs_forward_in_expr(expr):
      leaf_pair_list = list(leaf_pair)
      ## iterate chord pitches if first leaf is chord
      for pair in pitchtools.list_unordered_named_chromatic_pitch_pairs_in_expr(leaf_pair_list[0]):
         yield pair
      if isinstance(leaf_pair, set):
         for pair in pitchtools.list_unordered_named_chromatic_pitch_pairs_in_expr(leaf_pair):
            yield pair
      elif isinstance(leaf_pair, tuple):
         for pair in pitchtools.list_ordered_named_chromatic_pitch_pairs_from_expr_1_to_expr_2(*leaf_pair):
            yield pair
      else:
         raise TypeError('leaf pair must be set or tuple.')
      ## iterate chord pitches if last leaf is chord
      for pair in pitchtools.list_unordered_named_chromatic_pitch_pairs_in_expr(leaf_pair_list[1]):
         yield pair
