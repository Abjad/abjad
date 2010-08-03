from abjad.components._Measure.DynamicMeasure.DynamicMeasure import DynamicMeasure


## Staff promotion works here even on new staff types.     ##
## So long as your .ly \layout { } specification           ##
## causes new staff types to inherit from Staff somewhere. ##
 
class AnonymousMeasure(DynamicMeasure):
   r'''Dynamic measure with no time signature.  ::

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

   def __init__(self, music = None):
      '''Initialize music and hide TimeSignature stencil.'''
      from abjad.tools import overridetools
      DynamicMeasure.__init__(self, music = music)
      self.meter.stencil = False
      #self.meter.promote('stencil', 'Staff')
      overridetools.promote_attribute_to_context_on_grob_handler(self.meter, 'stencil', 'Staff')
