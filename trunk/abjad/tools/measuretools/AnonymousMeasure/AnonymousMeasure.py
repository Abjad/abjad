from abjad.tools.measuretools.DynamicMeasure.DynamicMeasure import DynamicMeasure


class AnonymousMeasure(DynamicMeasure):
   r'''Dynamic measure with no time signature:
   
   ::

      abjad> measure = AnonymousMeasure(macros.scale(4))
      abjad> f(measure)
      {
         \override Staff.TimeSignature #'stencil = ##f
         \time 1/2
         c'8
         d'8
         e'8
         f'8
         \revert Staff.TimeSignature #'stencil
      }

   ::
      
      abjad> measure.extend(macros.scale(2))
      abjad> f(measure)
      {
         \override Staff.TimeSignature #'stencil = ##f
         \time 3/4
         c'8
         d'8
         e'8
         f'8
         c'8
         d'8
         \revert Staff.TimeSignature #'stencil
      }
   '''

   def __init__(self, music = None, **kwargs):
      '''Initialize music and hide TimeSignature stencil.
      '''

      DynamicMeasure.__init__(self, music = music)
      self.override.staff.time_signature.stencil = False
      self._initialize_keyword_values(**kwargs)
