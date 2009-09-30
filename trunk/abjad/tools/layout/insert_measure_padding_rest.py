from abjad.rest import Rest
from abjad.tools.layout._insert_measure_padding import \
   _insert_measure_padding as layout__insert_measure_padding


def insert_measure_padding_rest(expr, front, back, splice = False):
   r'''.. versionadded:: 1.1.1

   Iterate all measures in `expr`. Insert rest with duration equal
   to `front` at beginning of each measure. Insert rest with
   duation aqual to `back` at end of each measure. 

   Set `front` to a positive rational or ``None``.
   Set `back` to a positive rational or ``None``.
   Return ``None``.

   .. note:: This function is designed to
      help create regularly spaced charts and tables of musical materials.
      This function makes most sense when used on
      :class:`~abjad.AnonymousMeasure`
      and :class:`~abjad.DynamicMeasure`
      instances.

   ::

      abjad> t = Staff(AnonymousMeasure(construct.scale(2)) * 2)
      abjad> front, back = Rational(1, 32), Rational(1, 64)
      abjad> layout.insert_measure_padding_rest(t, front, back)
      abjad> print t.format

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

   Works when measures contain stacked voices. ::

      abjad> measure = DynamicMeasure(Voice(construct.run(2)) * 2)
      abjad> measure.parallel = True
      abjad> t = Staff(measure * 2)
      abjad> pitchtools.diatonicize(t)
      abjad> layout.insert_measure_padding_rest(t, Rational(1, 32), Rational(1, 64))

   ::

      abjad> print t.format
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

      abjad> t = DynamicMeasure(construct.scale(2))
      abjad> Beam(t[:])
      abjad> t.formatter.number.self = 'comment'
      abjad> layout.insert_measure_padding_rest(t, Rational(1, 32), Rational(1, 64), splice = True)

   ::

      abjad> print t.format
      % start measure 1
         \time 19/64
         r32 [
         c'8
         d'8
         r64 ]
      % stop measure 1

   Raise :exc:`ValueError` when `front` is neither a positive
   rational nor ``None``.
   Raise :exc:`ValueError` when `back` is neither a positive
   rational nor ``None``. ::

      abjad> t = Staff(AnonymousMeasure(construct.scale(2)) * 2)
      abjad> layout.insert_measure_padding_rest(t, 'foo', 'bar')
      ValueError
   '''

   klass_token = Rest((1, 4))
   result = layout__insert_measure_padding(
      expr, front, back, klass_token, splice = splice)
   return result
