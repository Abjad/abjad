from abjad.tools.iterate._measure_get import _measure_get


def get_prev_measure_from_component(component):
   '''.. versionadded:: 1.1.1

   When `component` is voice, staff or other sequential context,
   and when `component` contains a measure, return last measure 
   in `component`. This starts the process of backwards measure iteration. ::

      abjad> staff = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 2)
      abjad> pitchtools.diatonicize(staff)
      abjad> iterate.get_prev_measure_from_component(staff)
      RigidMeasure(2/8, [e'8, f'8])

   When `component` is voice, staff or other sequential context,
   and when `component` contains no measure, 
   raise :exc:`MissingMeasureError`. ::

      abjad> staff = Staff(macros.scale(4))
      abjad> iterate.get_prev_measure_from_component(staff)
      MissingMeasureError

   When `component` is a measure and there is a measure immediately
   preceeding `component`, return measure immediately preceeding component. ::

      abjad> staff = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 2)
      abjad> pitchtools.diatonicize(staff)
      abjad> iterate.get_prev_measure_from_component(staff[-1])
      RigidMeasure(2/8, [c'8, d'8])

   When `component` is a measure and there is no measure immediately
   preceeding `component`, return ``None``. ::

      abjad> staff = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 2)
      abjad> pitchtools.diatonicize(staff)
      abjad> iterate.get_prev_measure_from_component(staff[0])
      (None)

   When `component` is a leaf and there is a measure in the parentage
   of `component`, return the measure in the parentage of `component`. ::

      abjad> staff = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 2)
      abjad> pitchtools.diatonicize(staff)
      abjad> iterate.get_prev_measure_from_component(staff.leaves[0])
      RigidMeasure(2/8, [c'8, d'8])

   When `component` is a leaf and there is no measure in the parentage
   of `component`, raise :exc:`MissingMeasureError`. ::

      abjad> staff = Staff(macros.scale(4))
      abjad> iterate.get_prev_measure_from_component(staff.leaves[0])
      MissingMeasureError

   .. versionchanged:: 1.1.2
      renamed ``iterate.measure_prev( )`` to
      ``iterate.get_prev_measure_from_component( )``.

   .. versionchanged:: 1.1.2
      renamed ``iterate.prev_measure_from_component( )`` to
      ``iterate.get_prev_measure_from_component( )``.
   '''

   return _measure_get(component, '_prev')
