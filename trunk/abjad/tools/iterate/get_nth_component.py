from abjad.tools.iterate.naive_backward_in import naive_backward_in as \
   iterate_naive_backward_in
from abjad.tools.iterate.naive_forward_in import naive_forward_in as \
   iterate_naive_forward_in


def get_nth_component(expr, klasses, n = 0):
   r'''.. versionadded:: 1.1.1

   Return element `n` in the `klasses` of `expr`. ::

      abjad> staff = Staff([ ])
      abjad> durations = [Rational(n, 16) for n in range(1, 5)]
      abjad> notes = construct.notes([0, 2, 4, 5], durations)
      abjad> rests = construct.rests(durations)
      abjad> leaves = listtools.interlace(notes, rests)
      abjad> staff.extend(leaves)

   ::

      abjad> print staff.format
      \new Staff {
              c'16
              r16
              d'8
              r8
              e'8.
              r8.
              f'4
              r4
      }
   
   ::
   
      abjad> for n in range(4):
      ...      iterate.get_nth_component(staff, Note, n)
      ...
      Note(c', 16)
      Note(d', 8)
      Note(e', 8.)
      Note(f', 4)

   ::

      abjad> for n in range(4):
      ...      iterate.get_nth_component(staff, Rest, n)
      ...
      Rest(16)
      Rest(8)
      Rest(8.)
      Rest(4)

   ::

      abjad> iterate.get_nth_component(staff, Staff)
      Staff{8}

   Read right-to-left for negative values of `n`. ::

      abjad> for n in range(3, -1, -1):
      ...      iterate.get_nth_component(staff, Rest, n)
      ...
      Rest(4)
      Rest(8.)
      Rest(8)
      Rest(16)      

   .. todo:: combine with :func:`~abjad.tools.scoretools.find`.

   .. versionchanged:: 1.1.2
      renamed ``iterate.get_nth( )`` to ``iterate.get_nth_component( )``.
   '''

   if not isinstance(n, (int, long)):
      raise ValueError

   if 0 <= n:
      for i, x in enumerate(iterate_naive_forward_in(expr, klasses)):
         if i == n:
            return x
   else:
      for i, x in enumerate(iterate_naive_backward_in(expr, klasses)):
         if i == abs(n) - 1:
            return x
