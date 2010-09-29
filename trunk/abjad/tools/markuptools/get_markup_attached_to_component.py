from abjad.tools.markuptools.Markup import Markup


def get_markup_attached_to_component(component):
   r'''.. versionadded:: 1.1.2

   Get markup attached to `component`::

      abjad> staff = Staff(macros.scale(4))
      abjad> slur = spannertools.SlurSpanner(staff.leaves)
      abjad> markuptools.Markup('comment 1')(staff[0])
      abjad> markuptools.Markup('comment 2')(staff[0])
      abjad> f(staff)
      \new Staff {
         %% comment 1
         %% comment 2
         c'8 (
         d'8
         e'8
         f'8 )
      }
      
   ::
      
      abjad> markuptools.get_markup_attached_to_component(staff[0]) 
      (Markup('comment 1')(c'8), Markup('comment 2')(c'8))

   Return tuple of zero or more markup objects.
   '''

   result = [ ]
   for mark in component._marks_for_which_component_functions_as_start_component:
      if isinstance(mark, Markup):
         result.append(mark)

   result = tuple(result)
   return result
