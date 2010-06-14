from abjad.tools import iterate
from abjad.tools.measuretools.color_measure import color_measure


def color_nonbinary_measures_in(expr, color = 'red'):
   r'''.. versionadded:: 1.1.2

   Color nonbinary measures in `expr` with `color`::

      abjad> staff = Staff(RigidMeasure((2, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(2)) * 2)
      abjad> measuretools.change_binary_measure_to_nonbinary(staff[1], 3)
      abjad> f(staff)
      \new Staff {
         {
            \time 2/8
            c'8
            d'8
         }
         {
            \time 3/12
            \scaleDurations #'(2 . 3) {
               c'8.
               d'8.
            }
         }
      }
      
   ::
      
      abjad> measuretools.color_nonbinary_measures_in(staff, 'red')
      [RigidMeasure(3/12(2))]
      
   ::
      
      abjad> f(staff)
      \new Staff {
         {
            \time 2/8
            c'8
            d'8
         }
         {
            \override Beam #'color = #red
            \override Dots #'color = #red
            \override Staff.TimeSignature #'color = #red
            \override NoteHead #'color = #red
            \override Stem #'color = #red
            \time 3/12
            \scaleDurations #'(2 . 3) {
               c'8.
               d'8.
            }
            \revert Beam #'color
            \revert Dots #'color
            \revert Staff.TimeSignature #'color
            \revert NoteHead #'color
            \revert Stem #'color
         }
      }

   Return list of measures colored.

   Color names appear in LilyPond Learning Manual appendix B.5.
   '''

   ## init measures colored
   measures_colored = [ ]

   ## color nonbinary measures in expr
   for measure in iterate.measures_forward_in(expr):
      if measure.meter.effective.nonbinary:
         color_measure(measure, color)
         measures_colored.append(measure)

   ## return measures colored
   return measures_colored
