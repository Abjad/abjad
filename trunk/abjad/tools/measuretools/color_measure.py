from abjad.components._Measure import _Measure
from abjad.tools import overridetools


def color_measure(measure, color = 'red'):
   r'''.. versionadded:: 1.1.2

   Color `measure` with `color`::

      abjad> measure = RigidMeasure((2, 8), macros.scale(2))
      abjad> f(measure)
      {
         \time 2/8
         c'8
         d'8
      }
      
   ::
      
      abjad> measuretools.color_measure(measure, 'red')
      RigidMeasure(2/8, [c'8, d'8])
      
   ::
      
      abjad> f(measure)
      {
         \override Beam #'color = #red
         \override Dots #'color = #red
         \override Staff.TimeSignature #'color = #red
         \override NoteHead #'color = #red
         \override Stem #'color = #red
         \time 2/8
         c'8
         d'8
         \revert Beam #'color
         \revert Dots #'color
         \revert Staff.TimeSignature #'color
         \revert NoteHead #'color
         \revert Stem #'color
      }

   Return colored `measure`.

   Color names appear in LilyPond Learning Manual appendix B.5.
   '''

   ## check measure type
   if not isinstance(measure, _Measure):
      raise TypeError('must be measure: %s' % measure)

   ## color measure
   measure.beam.color = color
   #measure.dots.color = color
   measure.override.dots.color = color
   measure.meter.color = color
   overridetools.promote_attribute_to_context_on_grob_handler(measure.meter, 'color', 'Staff')
   measure.note_head.color = color
   #measure.stem.color = color
   measure.override.stem.color = color

   ## return measure
   return measure
