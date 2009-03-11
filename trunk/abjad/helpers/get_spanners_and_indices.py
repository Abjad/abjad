from abjad.component.component import _Component


def _get_spanners_and_indices(component):
   '''Input parameters:
   
      component should be any Abjad component.

      Description:

      Return an unordered set of spanner, index pairs showing
      the different positions that component occupies within
      the set of zero or more spanners that attach to component.
      
      Intended sever possibly circular references from component 
      prior to making a deep copy of component and to enable
      the reinsertion of component within the spanners attaching
      to component after having made a deep copy of component.

      Example:

      t = RigidMeasure((5, 8), scale(5))
      beam = Beam(t[:])
      crescendo = Crescendo(t[:])
      glissando = Glissando(t[:])

      result = _get_spanners_and_indices(t[2])

      assert len(result) == 3
      assert (beam, 2) in result
      assert (crescendo, 2) in result
      assert (glissando, 2) in result'''

   # check input
   if not isinstance(component, _Component):
      raise ValueError('input must be an Abjad component.')

   # append spanner, index pairs to result
   result = [ ]   
   for spanner in component.spanners.attached:
      result.append((spanner, spanner.index(component)))

   # return result as an unordered set of spanner, index pairs
   return set(result)

