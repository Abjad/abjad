from abjad.measure.measure import _Measure
from abjad.rational import Rational
from abjad.rest import Rest
from abjad.tools import iterate
import types


def insert_measure_padding(expr, front, back):
   r'''Iterate all measures in `expr`. Insert transparent rest equal
   to `front` at beginning of each measure. Insert transparent 
   rest equal to `back` at end of each measure. 

   Set `front` to a positive rational or ``None``.
   Set `back` to a positive rational or ``None``.
   Return ``None``.

   .. note:: This function is designed to
      help create regularly spaced charts and tables of musical materials.
      This function makes most sense when used on
      :class:`~abjad.measure.anonymous.measure.AnonymousMeasure`
      and :class:`~abjad.measure.dynamic.measure.DynamicMeasure`
      instances.

   ::

      abjad> t = Staff(AnonymousMeasure(construct.scale(2)) * 2)
      abjad> front, back = Rational(1, 32), Rational(1, 64)
      abjad> layout.insert_measure_padding(t, front, back)
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

   Raise :exc:`ValueError` when `front` is neither a positive
   rational nor ``None``.
   Raise :exc:`ValueError` when `back` is neither a positive
   rational nor ``None``. ::

      abjad> t = Staff(AnonymousMeasure(construct.scale(2)) * 2)
      abjad> layout.insert_measure_padding(t, 'foo', 'bar')
      ValueError
   '''

   if not isinstance(front, (Rational, types.NoneType)):
      raise ValueError

   if not isinstance(back, (Rational, types.NoneType)):
      raise ValueError

   for measure in iterate.naive(expr, _Measure):
      if front is not None:
         front_rest = Rest(front)
         measure.insert(0, front_rest)
      if back is not None:
         back_rest = Rest(back)
         measure.append(back_rest)  
