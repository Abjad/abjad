def get_component_start_offset(component):
   r'''.. versionadded:: 1.1.1

   Get `component` start offset::

      abjad> staff = Staff(macros.scale(4))
      abjad> f(staff)
      \new Staff {
         c'8
         d'8
         e'8
         f'8
      }
      
   ::
      
      abjad> componenttools.get_component_start_offset(staff[1]) 
      Fraction(1, 8)

   Return nonnegative fraction.
   '''

   return component._offset.start
