from abjad.tools.iterate.measure_get import _measure_get


def measure_prev(component):
   '''When `component` is voice, staff or other sequential context,
   return last measure in context. 

   This starts the process of backwards measure iteration. ::

      abjad> staff = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
      abjad> pitchtools.diatonicize(staff)

   ::

      abjad> iterate.measure_prev(staff)
      RigidMeasure(2/8, [e'8, f'8])

   When `component` is a measure, return the measure immediately
   preceding `component`. ::

      abjad> iterate.measure_prev(_)    
      RigidMeasure(2/8, [c'8, d'8])

   Return ``None`` When `component` is a measure and no measure 
   immediately precedes `component`. ::

      abjad> iterate.measure_prev(_)
      (None)
   '''

   return _measure_get(component, '_prev')
