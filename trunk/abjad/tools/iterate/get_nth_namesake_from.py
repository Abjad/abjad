from abjad.tools.iterate.namesakes_backward_from import namesakes_backward_from
from abjad.tools.iterate.namesakes_forward_from import namesakes_forward_from


def get_nth_namesake_from(component, n):
   '''.. versionadded:: 1.1.2

   For positive `n`, return namesake to the right of `component`. ::

      abjad> t = Staff(construct.scale(4))
      abjad> iterate.get_nth_namesake_from(t[1], 1)
      Note(e', 8)

   For negative `n`, return namesake to the left of `component`. ::

      abjad> t = Staff(construct.scale(4))
      abjad> iterate.get_nth_namesake_from(t[1], -1)
      Note(c', 8)

   Return `component` when `n` is zero. ::

      abjad> t = Staff(construct.scale(4))
      abjad> iterate.get_nth_namesake_from(t[1], 0)
      Note(d', 8)
   '''

   if 0 <= n:
      for i, namesake in enumerate(namesakes_forward_from(component)):
         if i == n:
            return namesake
   else:
      n = abs(n)
      for i, namesake in enumerate(namesakes_backward_from(component)):
         if i == n:
            return namesake

   raise IndexError('only %s namesakes from %s, not %s.' % (i, component, n))
