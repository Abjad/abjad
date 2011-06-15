from abjad.tools.layouttools._insert_measure_padding import _insert_measure_padding
from abjad.tools.skiptools.Skip import Skip


def pad_measures_in_expr_with_skips(expr, front, back, splice = False):
   r'''.. versionadded:: 1.1.2

   Iterate all measures in `expr`. Insert skip with duration equal
   to `front` at beginning of each measure. Insert skip with
   duation aqual to `back` at end of each measure. 

   Set `front` to a positive rational or none.
   Set `back` to a positive rational or none.
   Return none.

   .. note:: This function is designed to
      help create regularly spaced charts and tables of musical materials.
      This function makes most sense when used on
      :class:`~abjad.AnonymousMeasure`
      and :class:`~abjad.DynamicMeasure`
      instances.

   ::

      abjad> t = Staff(measuretools.AnonymousMeasure("c'8 d'8") * 2)
      abjad> front, back = Duration(1, 32), Duration(1, 64)
      abjad> measuretools.pad_measures_in_expr_with_skips(t, front, back) # doctest: +SKIP
      abjad> f(t) # doctest: +SKIP
      \new Staff {
                      \override Staff.TimeSignature #'stencil = ##f
                      \time 19/64
                      s32
                      c'8
                      d'8
                      s64
                      \revert Staff.TimeSignature #'stencil
                      \override Staff.TimeSignature #'stencil = ##f
                      \time 19/64
                      s32
                      c'8
                      d'8
                      s64
                      \revert Staff.TimeSignature #'stencil
      }

   Works when measures contain stacked voices. ::

      abjad> measure = measuretools.DynamicMeasure(Voice(notetools.make_repeated_notes(2)) * 2)
      abjad> measure.is_parallel = True
      abjad> t = Staff(measure * 2)
      abjad> macros.diatonicize(t)
      abjad> measuretools.pad_measures_in_expr_with_skips(t, Duration(1, 32), Duration(1, 64)) # doctest: +SKIP

   ::

      abjad> f(t) # doctest: +SKIP
      \new Staff {
            \time 19/64
            \new Voice {
               s32
               c'8
               d'8
               s64
            }
            \new Voice {
               s32
               e'8
               f'8
               s64
            }
            \time 19/64
            \new Voice {
               s32
               g'8
               a'8
               s64
            }
            \new Voice {
               s32
               b'8
               c''8
               s64
            }
      }

   Set the optional `splice` keyword to ``True`` to extend edge
   spanners over newly inserted skips. ::

      abjad> t = measuretools.DynamicMeasure("c'8 d'8")
      abjad> spannertools.BeamSpanner(t[:])
      BeamSpanner(c'8, d'8)
      abjad> t.formatter.number.self = 'comment' # doctest: +SKIP
      abjad> measuretools.pad_measures_in_expr_with_skips(t, Duration(1, 32), Duration(1, 64), splice = True) # doctest: +SKIP

   ::

      abjad> f(t) # doctest: +SKIP
      % start measure 1
         \time 19/64
         s32 [
         c'8
         d'8
         s64 ]
      % stop measure 1

   Raise value error when `front` is neither a positive rational nor none.

   Raise value error when `back` is neither a positive rational nor none.

   .. versionchanged:: 1.1.2
      renamed ``layout.insert_measure_padding_skip( )`` to
      ``measuretools.pad_measures_in_expr_with_skips( )``.
   '''

   klass_token = Skip((1, 4))
   result = _insert_measure_padding(expr, front, back, klass_token, splice = splice)
   return result
