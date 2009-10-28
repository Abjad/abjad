from abjad.tools.iterate.naive_backward import naive_backward as \
   iterate_naive_backward
from abjad.tools.iterate.naive_forward import naive_forward as \
   iterate_naive_forward


def get_nth(expr, klasses, n = 0):
   r'''.. versionadded:: 1.1.1

   .. todo:: combine with :func:`~abjad.tools.scoretools.find.find`.

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
      ...      iterate.get_nth(staff, Note, n)
      ...
      Note(c', 16)
      Note(d', 8)
      Note(e', 8.)
      Note(f', 4)

   ::

      abjad> for n in range(4):
      ...      iterate.get_nth(staff, Rest, n)
      ...
      Rest(16)
      Rest(8)
      Rest(8.)
      Rest(4)

   ::

      abjad> iterate.get_nth(staff, Staff)
      Staff{8}

   Read right-to-left for negative values of `n`. ::

      abjad> for n in range(3, -1, -1):
      ...      iterate.get_nth(staff, Rest, n)
      ...
      Rest(4)
      Rest(8.)
      Rest(8)
      Rest(16)      

   .. note:: Because this function returns as soon as it finds instance
      `n` of `klasses`, it is more efficient to call
      ``iterate.get_nth(expr, _Leaf, 0)`` than ``expr.leaves[0]``.
      It is likewise more efficient to call
      ``iterate.get_nth(expr, _Leaf, -1)`` than ``expr.leaves[-1]``.
   '''

   if not isinstance(n, (int, long)):
      raise ValueError

   if 0 <= n:
      for i, x in enumerate(iterate_naive_forward(expr, klasses)):
         if i == n:
            return x
   else:
      for i, x in enumerate(iterate_naive_backward(expr, klasses)):
         if i == abs(n) - 1:
            return x
