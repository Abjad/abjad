from abjad.tools.iterate._measure_get import _measure_get


def measure_next(component):
   '''.. versionadded:: 1.1.1

   When `component` is voice, staff or other sequential context,
   and when `component` contains a measure, return first measure 
   in `component`. This starts the process of forwards measure iteration. ::

      abjad> staff = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
      abjad> pitchtools.diatonicize(staff)
      abjad> iterate.measure_next(staff)
      RigidMeasure(2/8, [c'8, d'8])

   When `component` is voice, staff or other sequential context,
   and when `component` contains no measure, 
   raise :exc:`MissingMeasureError`. ::

      abjad> staff = Staff(construct.scale(4))
      abjad> iterate.measure_next(staff)
      MissingMeasureError

   When `component` is a measure and there is a measure immediately
   following `component`, return measure immediately following component. ::

      abjad> staff = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
      abjad> pitchtools.diatonicize(staff)
      abjad> iterate.measure_prev(staff[0])
      RigidMeasure(2/8, [e'8, f'8])

   When `component` is a measure and there is no measure immediately
   following `component`, return ``None``. ::

      abjad> staff = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
      abjad> pitchtools.diatonicize(staff)
      abjad> iterate.measure_prev(staff[-1])
      (None)

   When `component` is a leaf and there is a measure in the parentage
   of `component`, return the measure in the parentage of `component`. ::

      abjad> staff = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
      abjad> pitchtools.diatonicize(staff)
      abjad> iterate.measure_prev(staff.leaves[0])
      RigidMeasure(2/8, [c'8, d'8])

   When `component` is a leaf and there is no measure in the parentage
   of `component`, raise :exc:`MissingMeasureError`. ::

      abjad> staff = Staff(construct.scale(4))
      abjad> iterate.measure_prev(staff.leaves[0])
      MissingMeasureError
   '''

   return _measure_get(component, '_next')
