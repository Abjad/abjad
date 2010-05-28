def flip(component):
   r'''Flip `component` one index to the right in parent and spanners. ::

      abjad> t = Voice(construct.scale(4))
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
      
      abjad> componenttools.flip(t[1])
      abjad> f(t)
      \new Voice {
         c'8 [
         e'8 ]
         d'8 [
         f'8 ]
      }

   Return none.

   .. todo:: add ``n = 1`` keyword to generalize flipped distance.
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
      spanner._severComponent(component)
   next_spanners = { }
   for spanner in list(next.spanners.attached):
      next_spanners[spanner] = spanner.index(next)
      spanner._severComponent(next)
   for key, value in next_spanners.items( ):
      key._insert(value, component)
   for key, value in component_spanners.items( ):
      key._insert(value, next)
