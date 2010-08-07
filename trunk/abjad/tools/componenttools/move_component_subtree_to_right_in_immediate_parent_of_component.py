def move_component_subtree_to_right_in_immediate_parent_of_component(component):
   r'''Flip `component` one index to the right in parent and spanners. ::

      abjad> t = Voice(macros.scale(4))
      abjad> Beam(t[:2])
      abjad> Beam(t[2:])
      abjad> f(t)
      \new Voice {
         c'8 [
         d'8 ]
         e'8 [
         f'8 ]
      }
      
   ::
      
      abjad> componenttools.move_component_subtree_to_right_in_immediate_parent_of_component(t[1])
      abjad> f(t)
      \new Voice {
         c'8 [
         e'8 ]
         d'8 [
         f'8 ]
      }

   Return none.

   .. todo:: add ``n = 1`` keyword to generalize flipped distance.

   .. todo:: make ``componenttools.move_component_subtree_to_right_in_immediate_parent_of_component( )`` work when spanners
      attach to children of component:

   ::

      abjad> voice = Voice(FixedDurationTuplet((2, 8), leaftools.make_repeated_notes(3)) * 2)
      abjad> Beam(voice.leaves[:4])
      abjad> pitchtools.diatonicize(voice)
      abjad> componenttools.move_component_subtree_to_right_in_immediate_parent_of_component(voice[0])
      abjad> f(voice)
      \new Voice {
         \times 2/3 {
            f'8 ]
            g'8
            a'8
         }
         \times 2/3 {
            c'8 [
            d'8
            e'8
         }
      }
      abjad> componenttools.is_well_formed_component(voice) 
      False   

   .. versionchanged:: 1.1.2
      renamed ``componenttools.flip( )`` to
      ``componenttools.move_component_subtree_to_right_in_immediate_parent_of_component( )``.

   .. versionchanged:: 1.1.2
      renamed ``componenttools.move_component_subtree_to_right_in_score_and_spanners( )`` to
      ``componenttools.move_component_subtree_to_right_in_immediate_parent_of_component( )``.
   '''

   # swap positions in parent
   if not component.parentage.orphan:
      parent = component.parentage.parent
      parent_index = parent.index(component)
      try:
         next = parent[parent_index + 1]
      except IndexError:
         return
      parent._music[parent_index] = next
      parent._music[parent_index + 1] = component

   # swap positions in spanners ... tricky!
   component_spanners = { }
   for spanner in list(component.spanners.attached):
      component_spanners[spanner] = spanner.index(component)
      spanner._sever_component(component)
   next_spanners = { }
   for spanner in list(next.spanners.attached):
      next_spanners[spanner] = spanner.index(next)
      spanner._sever_component(next)
   for key, value in next_spanners.items( ):
      key._insert(value, component)
   for key, value in component_spanners.items( ):
      key._insert(value, next)
