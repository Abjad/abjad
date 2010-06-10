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

   .. todo:: make ``componenttools.flip( )`` work when spanners
      attach to children of component:

   ::

      abjad> voice = Voice(FixedDurationTuplet((2, 8), construct.run(3)) * 2)
      abjad> Beam(voice.leaves[:4])
      abjad> pitchtools.diatonicize(voice)
      abjad> componenttools.flip(voice[0])
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
      abjad> check.wf(voice) 
      False   
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
