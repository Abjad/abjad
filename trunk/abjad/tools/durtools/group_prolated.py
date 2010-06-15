#from abjad.tools.componenttools._group_components_by_durations \
#   import _group_components_by_durations


def group_prolated(
   components, durations, fill = 'exact', cyclic = False, overhang = False):
   r'''Group `components` according to prolated `durations`.

   * When ``fill = exact``, parts must equal `durations` exactly.
   * When ``fill = less``, parts must be ``<= durations``.
   * When ``fill = greater``, parts must be ``>= durations``.
   * If ``cyclic = True``, read `durations` cyclically.
   * If ``overhang = True`` and components remain, append final part.
   * If ``overhang = False`` and components remain, do not append final part.

   Examples all refer to the following. ::

      abjad> t = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 4)
      abjad> pitchtools.diatonicize(t)
      abjad> f(t)
      \new Staff {
              {
                      \time 2/8
                      c'8
                      d'8
              }
              {
                      \time 2/8
                      e'8
                      f'8
              }
              {
                      \time 2/8
                      g'8
                      a'8
              }
              {
                      \time 2/8
                      b'8
                      c''8
              }
      }

   Noncyclic exact fill with no overhang part. ::

      abjad> durtools.group_prolated(t.leaves, [Rational(3, 8)], fill = 'exact', cyclic = False, overhang = False)
      [[Note(c', 8), Note(d', 8), Note(e', 8)]]

   Noncyclic exact fill with overhang part. ::

      abjad> durtools.group_prolated(t.leaves, [Rational(3, 8)], fill = 'exact', cyclic = False, overhang = True)
      [[Note(c', 8), Note(d', 8), Note(e', 8)], [Note(f', 8), Note(g', 8), Note(a', 8), Note(b', 8), Note(c'', 8)]]

   Cyclic exact fill with no overhang part. ::

      abjad> durtools.group_prolated(t.leaves, [Rational(3, 8)], fill = 'exact', cyclic = True, overhang = False)
      [[Note(c', 8), Note(d', 8), Note(e', 8)], [Note(f', 8), Note(g', 8), Note(a', 8)]]

   Cyclic exact fill with overhang part. ::

      abjad> durtools.group_prolated(t.leaves, [Rational(3, 8)], fill = 'exact', cyclic = True, overhang = True)
      [[Note(c', 8), Note(d', 8), Note(e', 8)], [Note(f', 8), Note(g', 8), Note(a', 8)], [Note(b', 8), Note(c'', 8)]]   
   '''
   from abjad.tools.componenttools._group_components_by_durations \
      import _group_components_by_durations
   
   duration_type = 'prolated'

   return _group_components_by_durations(duration_type,
      components, durations, fill = fill, cyclic = cyclic, overhang = overhang)
