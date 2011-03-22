from abjad.exceptions import ExtraMarkError


def get_effective_context_mark(component, klass):
   r'''.. versionadded:: 1.1.2

   Get effective context mark of `klass` from `component`::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")
      abjad> contexttools.TimeSignatureMark(4, 8)(staff)
      TimeSignatureMark(4, 8)(Staff{4})

   ::

      abjad> f(staff)
      \new Staff {
         \time 4/8
         c'8
         d'8
         e'8
         f'8
      }

   ::

      abjad> contexttools.get_effective_context_mark(staff[0], contexttools.TimeSignatureMark)
      TimeSignatureMark(4, 8)(Staff{4})


   Return context mark or none.
   '''
   from abjad.components import Measure
   from abjad.tools import componenttools
   from abjad.tools.contexttools.TimeSignatureMark import TimeSignatureMark

   #print 'getting ready to get effective mark ...'
   component._update_prolated_offset_values_of_entire_score_tree_if_necessary( )
   component._update_marks_of_entire_score_tree_if_necessary( )

   #print 'now getting effective mark ...'
   candidate_marks = set([ ])
   for parent in componenttools.get_improper_parentage_of_component(component):
      for mark in parent.marks:
         if isinstance(mark, klass):
            if mark.effective_context is not None:
               candidate_marks.add(mark)
            elif isinstance(mark, TimeSignatureMark):
               if isinstance(mark.start_component, Measure):
                  candidate_marks.add(mark)
   candidate_marks = sorted(candidate_marks, 
      cmp = lambda m, n: cmp(m.start_component._offset.start, n.start_component._offset.start)) 
   #print candidate_marks
   #for x in candidate_marks:
   #   print x, x.start_component._offset.start
   first_winner = None
   for candidate_mark in reversed(candidate_marks):
      if candidate_mark.start_component._offset.start <= component._offset.start:
         if first_winner is None:
            first_winner = candidate_mark
         elif candidate_mark.start_component._offset.start == \
            first_winner.start_component._offset.start:
            raise ExtraMarkError('%s and %s start at the same time.' % (
               first_winner, candidate_mark))
         else:
            break
   #print 'first winner is ', first_winner, '\n'
   return first_winner
