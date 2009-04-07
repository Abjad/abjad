from abjad.measure.dynamic.measure import DynamicMeasure


## Staff promotion works here even on new staff types.     ##
## So long as your .ly \layout { } specification           ##
## causes new staff types to inherit from Staff somewhere. ##
 
class AnonymousMeasure(DynamicMeasure):
   '''Measure that dynamically grows and shrinks.
      Measure that also always hides TimeSignature stencil.'''

   def __init__(self, music = None):
      '''Initialize music and hide TimeSignature stencil.'''
      DynamicMeasure.__init__(self, music = music)
      self.meter.stencil = False
      self.meter.promote('stencil', 'Staff')
