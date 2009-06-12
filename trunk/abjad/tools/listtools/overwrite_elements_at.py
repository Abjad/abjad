import sys
import types


def overwrite_elements_at(l, indices, material):
   '''Overwrite elements in *l* at cyclic *indices* with cyclic *material*.

   ::

      abjad> l = range(20)
      abjad> listtools.overwrite_elements_at(l, ([0], 2), (['A', 'B'], 3))
      ['A', 1, 'B', 3, 4, 5, 'A', 7, 'B', 9, 10, 11, 'A', 13, 'B', 15, 16, 17, 'A', 19]

   ::

      abjad> l = range(20)
      abjad> listtools.overwrite_elements_at(l, ([0], 2), (['*'], 1))
      ['*', 1, '*', 3, '*', 5, '*', 7, '*', 9, '*', 11, '*', 13, '*', 15, '*', 17, '*', 19]

   ::

      abjad> l = range(20)
      abjad> listtools.overwrite_elements_at(l, ([0], 2), (['A', 'B', 'C', 'D'], None))
      ['A', 1, 'B', 3, 'C', 5, 'D', 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

   ::

      abjad> l = range(20)
      abjad> listtools.overwrite_elements_at(l, ([0, 1, 8, 13], None), (['A', 'B', 'C', 'D'], None))
      ['A', 'B', 2, 3, 4, 5, 6, 7, 'C', 9, 10, 11, 12, 'D', 14, 15, 16, 17, 18, 19]

   Raise :exc:`TypeError` when *l* is not a list::

      abjad> listtools.overwrite_elements_at('foo', ([0], 2), (['*'], 1))
      TypeError
   '''

   if not isinstance(l, list):
      raise TypeError

   assert isinstance(indices, tuple) and len(indices) == 2
   index_values, index_period = indices

   assert isinstance(index_values, list)
   assert isinstance(index_period, (int, long, types.NoneType))

   assert isinstance(material, tuple) and len(material) == 2
   material_values, material_period = material

   assert isinstance(material_values, list)
   assert isinstance(material_period, (int, long, types.NoneType))

   if index_period is None:
      index_period = sys.maxint

   if material_period is None:
      material_period = sys.maxint

   result = [ ]

   material_index = 0

   for index, element in enumerate(l):
      if index % index_period in index_values:
         try:
            cyclic_material_index = material_index % material_period
            material_value = material_values[cyclic_material_index]
            result.append(material_value)
         except IndexError:
            result.append(element)   
         material_index += 1
      else:
         result.append(element)

   return result
