def get_improper_parentage_of_component(component):
   '''Get improper parentage of `component`:

   ::

      abjad> tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
      abjad> staff = Staff([tuplet])
      abjad> note = staff.leaves[0]
      abjad> note.parentage.improper_parentage
      [Note(c', 8), tuplettools.FixedDurationTuplet(1/4, [c'8, d'8, e'8]), Staff{1}]

   .. versionchanged:: 1.1.1
      Returns (immutable) tuple instead of (mutable) list.
   '''

   result = [ ]
   parent = component
   while parent is not None:
      result.append(parent)
      parent = parent.parentage.parent
   result = tuple(result)
   return result
