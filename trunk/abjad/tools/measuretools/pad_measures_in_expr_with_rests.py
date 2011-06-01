from abjad.components import Rest
from abjad.tools.layouttools._insert_measure_padding import _insert_measure_padding


def pad_measures_in_expr_with_rests(expr, front, back, splice = False):
   r'''.. versionadded:: 1.1.1

   Iterate all measures in `expr`. Insert rest with duration equal
   to `front` at beginning of each measure. Insert rest with
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

      abjad> t = Staff(measuretools.AnonymousMeasure(macros.scale(2)) * 2)
      abjad> front, back = Fraction(1, 32), Fraction(1, 64)
      abjad> measuretools.pad_measures_in_expr_with_rests(t, front, back) # doctest: +SKIP
      abjad> f(t) # doctest: +SKIP
      \new Staff {
                      \override Staff.TimeSignature #'stencil = ##f
                      \time 19/64
                      r32
                      c'8
                      d'8
                      r64
                      \revert Staff.TimeSignature #'stencil
                      \override Staff.TimeSignature #'stencil = ##f
                      \time 19/64
                      r32
                      c'8
                      d'8
                      r64
                      \revert Staff.TimeSignature #'stencil
      }

   Works when measures contain stacked voices::

      abjad> measure = measuretools.DynamicMeasure(Voice(notetools.make_repeated_notes(2)) * 2)
      abjad> measure.is_parallel = True
      abjad> t = Staff(measure * 2)
      abjad> macros.diatonicize(t)
      abjad> measuretools.pad_measures_in_expr_with_rests(t, Fraction(1, 32), Fraction(1, 64)) # doctest: +SKIP

   ::

      abjad> f(t) # doctest: +SKIP
      \new Staff {
            \time 19/64
            \new Voice {
               r32
               c'8
               d'8
               r64
            }
            \new Voice {
               r32
               e'8
               f'8
               r64
            }
            \time 19/64
            \new Voice {
               r32
               g'8
               a'8
               r64
            }
            \new Voice {
               r32
               b'8
               c''8
               r64
            }
      }

   Set the optional `splice` keyword to ``True`` to extend edge
   spanners over newly inserted rests. ::

      abjad> t = measuretools.DynamicMeasure(macros.scale(2))
      abjad> spannertools.BeamSpanner(t[:])
      BeamSpanner(c'8, d'8)
      abjad> t.formatter.number.self = 'comment' # doctest: +SKIP
      abjad> measuretools.pad_measures_in_expr_with_rests(t, Fraction(1, 32), Fraction(1, 64), splice = True) # doctest: +SKIP

   ::

      abjad> f(t) # doctest: +SKIP
      % start measure 1
         \time 19/64
         r32 [
         c'8
         d'8
         r64 ]
      % stop measure 1

   Raise value when `front` is neither a positive rational nor none.

   Raise value when `back` is neither a positive rational nor none.

   .. versionchanged:: 1.1.2
      renamed ``layout.insert_measure_padding_rest( )`` to
      ``measuretools.pad_measures_in_expr_with_rests( )``.
   '''

   klass_token = Rest((1, 4))
   result = _insert_measure_padding(expr, front, back, klass_token, splice = splice)
   return result
