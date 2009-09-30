from abjad.leaf.leaf import _Leaf
from abjad.measure.measure import _Measure
from abjad.rational import Rational
from abjad.skip import Skip
from abjad.tools import iterate
import types


def insert_measure_padding_skip(expr, front, back, splice = False):
   r'''.. versionadded:: 1.1.1

   Iterate all measures in `expr`. Insert skip with duration equal
   to `front` at beginning of each measure. Insert skip with
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
      abjad> layout.insert_measure_padding_skip(t, front, back)
      abjad> print t.format

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

      abjad> measure = DynamicMeasure(Voice(construct.run(2)) * 2)
      abjad> measure.parallel = True
      abjad> t = Staff(measure * 2)
      abjad> pitchtools.diatonicize(t)
      abjad> layout.insert_measure_padding_skip(t, Rational(1, 32), Rational(1, 64))

   ::

      abjad> print t.format
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

      abjad> t = DynamicMeasure(construct.scale(2))
      abjad> Beam(t[:])
      abjad> t.formatter.number.self = 'comment'
      abjad> layout.insert_measure_padding_skip(t, Rational(1, 32), Rational(1, 64), splice = True)

   ::

      abjad> print t.format
      % start measure 1
         \time 19/64
         s32 [
         c'8
         d'8
         s64 ]
      % stop measure 1

   Raise :exc:`ValueError` when `front` is neither a positive
   rational nor ``None``.
   Raise :exc:`ValueError` when `back` is neither a positive
   rational nor ``None``. ::

      abjad> t = Staff(AnonymousMeasure(construct.scale(2)) * 2)
      abjad> layout.insert_measure_padding_skip(t, 'foo', 'bar')
      ValueError
   '''

   if not isinstance(front, (Rational, types.NoneType)):
      raise ValueError

   if not isinstance(back, (Rational, types.NoneType)):
      raise ValueError

   root = expr[0].parentage.root

   ## forbid updates because _Component.splice_left( ) and ##
   ## _Component.splice( ) call self.offset.prolated.stop  ##
   root._update._forbidUpdate( )

   for measure in iterate.naive(expr, _Measure):
      if front is not None:
         start_components = measure._navigator._contemporaneousStartContents
         start_leaves = [x for x in start_components if isinstance(x, _Leaf)]
         for start_leaf in start_leaves:
            if splice:
               start_leaf.splice_left([Skip(front)])
            else:
               start_leaf.extend_left_in_parent([Skip(front)])
      if back is not None:
         stop_components = measure._navigator._contemporaneousStopContents
         stop_leaves = [x for x in stop_components if isinstance(x, _Leaf)]
         for stop_leaf in stop_leaves:
            if splice:
               stop_leaf.splice([Skip(back)])
            else:
               stop_leaf.extend_in_parent([Skip(back)])

   ## allow updates after all calls to splice( ) are done. ##
   root._update._allowUpdate( )
