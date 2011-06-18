from abjad.tools.componenttools._Component import _Component


def component_to_pitch_and_rhythm_skeleton_with_interface_attributes(component):
   r'''.. versionadded:: 1.1.2

   Change `component` to pitch and rhythm skeleton with interface attributes.

   Return string.

   .. note:: function currently not working.
   '''
   from abjad.tools.leaftools._Leaf import _Leaf
   from abjad.tools.containertools._container_to_pitch_and_rhythm_skeleton import _container_to_pitch_and_rhythm_skeleton
   from abjad.tools.leaftools._leaf_to_pitch_and_rhythm_skeleton import _leaf_to_pitch_and_rhythm_skeleton
   
   if not isinstance(component, _Component):
      raise TypeError('must be Abjad component.')

   if isinstance(component, _Leaf):
      return _leaf_to_pitch_and_rhythm_skeleton(component, include_keyword_attributes = True)
   else:
      return _container_to_pitch_and_rhythm_skeleton(component, include_keyword_attributes = True)
