from abjad.tools.measuretools._measure_get import _measure_get


def get_next_measure_from_component(component):
   '''.. versionadded:: 1.1.1

   When `component` is voice, staff or other sequential context,
   and when `component` contains a measure, return first measure 
   in `component`. This starts the process of forwards measure iteration. ::

      abjad> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
      abjad> macros.diatonicize(staff)
      abjad> measuretools.get_next_measure_from_component(staff)
      Measure(2/8, [c'8, d'8])

   When `component` is voice, staff or other sequential context,
   and when `component` contains no measure, 
   raise :exc:`MissingMeasureError`. ::

      abjad> staff = Staff(macros.scale(4))
      abjad> measuretools.get_next_measure_from_component(staff)
      MissingMeasureError

   When `component` is a measure and there is a measure immediately
   following `component`, return measure immediately following component. ::

      abjad> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
      abjad> macros.diatonicize(staff)
      abjad> measuretools.get_prev_measure_from_component(staff[0])
      Measure(2/8, [e'8, f'8])

   When `component` is a measure and there is no measure immediately
   following `component`, return ``None``. ::

      abjad> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
      abjad> macros.diatonicize(staff)
      abjad> measuretools.get_prev_measure_from_component(staff[-1])
      (None)

   When `component` is a leaf and there is a measure in the parentage
   of `component`, return the measure in the parentage of `component`. ::

      abjad> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
      abjad> macros.diatonicize(staff)
      abjad> measuretools.get_prev_measure_from_component(staff.leaves[0])
      Measure(2/8, [c'8, d'8])

   When `component` is a leaf and there is no measure in the parentage
   of `component`, raise :exc:`MissingMeasureError`. ::

      abjad> staff = Staff(macros.scale(4))
      abjad> measuretools.get_prev_measure_from_component(staff.leaves[0])
      MissingMeasureError

   .. versionchanged:: 1.1.2
      renamed ``iterate.measure_next( )`` to
      ``measuretools.get_next_measure_from_component( )``.

   .. versionchanged:: 1.1.2
      renamed ``iterate.next_measure_from_component( )`` to
      ``measuretools.get_next_measure_from_component( )``.

   .. versionchanged:: 1.1.2
      renamed ``iterate.get_next_measure_from_component( )`` to
      ``measuretools.get_next_measure_from_component( )``.
   '''

   return _measure_get(component, '_next')
