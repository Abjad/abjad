from abjad.tools.marktools.get_comments_attached_to_component import get_comments_attached_to_component


def detach_comments_attached_to_component(component):
   r'''.. versionadded:: 1.1.2
   
   Detach comments attached to `component`::

      abjad> staff = Staff(macros.scale(4))
      abjad> slur = spannertools.SlurSpanner(staff.leaves)
      abjad> marktools.Comment('comment 1')(staff[0])
      abjad> marktools.Comment('comment 2')(staff[0])

   ::

      abjad> f(staff)
      \new Staff {
         % comment 1
         % comment 2
         c'8 (
         d'8
         e'8
         f'8 )
      }
      
   ::
      
      abjad> marktools.detach_comments_attached_to_component(staff[0]) 
      (Comment('comment 1'), Comment('comment 2'))
      
   ::
      
      abjad> f(staff)
      \new Staff {
         c'8 (
         d'8
         e'8
         f'8 )
      }

   ::
      
      abjad> marktools.get_comments_attached_to_component(staff[0]) 
      ()

   Return tuple or zero or more comments.
   '''

   comments = [ ]
   for comment in get_comments_attached_to_component(component):
      comment.detach_mark( )
      comments.append(comment)

   return tuple(comments)
