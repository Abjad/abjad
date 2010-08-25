from abjad.exceptions import ExtraMarkError


def get_effective_mark(component, klass):
   '''.. versionadded:: 1.1.2

   Get effective mark of mark `klass` for `component`.
   '''

   candidate_marks = set([ ])
   for parent in component.parentage.improper_parentage:
      #print parent
      for mark in parent.marks:
         if isinstance(mark, klass):
            candidate_marks.add(mark)
   candidate_marks = sorted(candidate_marks, 
      cmp = lambda m, n: cmp(m.start_component.offset.start, n.start_component.offset.start)) 
   #for x in candidate_marks:
   #   print x, x.start_component.offset.start
   #print ''
   first_winner = None
   for candidate_mark in reversed(candidate_marks):
      if candidate_mark.start_component.offset.start <= component.offset.start:
         if first_winner is None:
            first_winner = candidate_mark
         elif candidate_mark.start_component.offset.start == \
            first_winner.start_component.offset.start:
            raise ExtraMarkError('%s and %s start at the same time.' % (
               first_winner, candidate_mark))
         else:
            break
   return first_winner
