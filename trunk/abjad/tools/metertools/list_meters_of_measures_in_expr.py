def list_meters_of_measures_in_expr(components):
   '''Extract ordered list of meter pairs from ``components``.

   Example::

      abjad> t = Staff([Measure((2, 8), macros.scale(2)),
         Measure((3, 8), macros.scale(3)),
         Measure((4, 8), macros.scale(4))])

      abjad> metertools.list_meters_of_measures_in_expr(t[:])
      [(2, 8), (3, 8), (4, 8)]

   Useful as input to some rhythmic transforms.

   .. versionchanged:: 1.1.2
      renamed ``metertools.extract_meter_list( )`` to
      ``metertools.list_meters_of_measures_in_expr( )``.

   .. versionchanged:: 1.1.2
      renamed ``metertools.extract_meters_from_measures_in_expr( )`` to
      ``metertools.list_meters_of_measures_in_expr( )``.
   '''
   from abjad.tools import componenttools
   from abjad.tools import marktools
   from abjad.tools import measuretools

   ## make sure components is a Python list of Abjad components
   assert componenttools.all_are_components(components)

   ## create empty list to hold result
   result = [ ]

   ## iterate measures and store meter pairs
   for measure in measuretools.iterate_measures_forward_in_expr(components):
      meter = marktools.get_effective_time_signature(measure)
      pair = (meter.numerator, meter.denominator)
      result.append(pair)

   ## return result
   return result
