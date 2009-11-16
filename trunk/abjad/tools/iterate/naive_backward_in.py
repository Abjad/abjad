from abjad.leaf import _Leaf


def naive_backward_in(expr, klass = _Leaf, start = 0, stop = None):
   r'''Yield right-to-left instances of `klass` in `expr`.

   ::

      abjad> staff = Staff(FixedDurationTuplet((2, 8), construct.run(3)) * 2)
      abjad> pitchtools.diatonicize(staff)
      abjad> f(staff)
      \new Staff {
              \times 2/3 {
                      c'8
                      d'8
                      e'8
              }
              \times 2/3 {
                      f'8
                      g'8
                      a'8
              }
      }
      abjad> for x in iterate.naive_backward_in(staff, Note):
      ...     x 
      ... 
      Note(a', 8)
      Note(g', 8)
      Note(f', 8)
      Note(e', 8)
      Note(d', 8)
      Note(c', 8)

   .. versionadded:: 1.1.2
      optional `start` and `stop` keyword parameters.

   ::

      abjad> for x in iterate.naive_backward_in(staff, Note, start = 0, stop = 4):
      ...     x
      ... 
      Note(c'', 8)
      Note(b', 8)
      Note(a', 8)
      Note(g', 8)

   ::

      abjad> for x in iterate.naive_backward_in(staff, Note, start = 4):
      ...     x
      ... 
      Note(f', 8)
      Note(e', 8)
      Note(d', 8)
      Note(c', 8)

   ::

      abjad> for x in iterate.naive_backward_in(staff, Note, start = 4, stop = 6):
      ...     x
      ... 
      Note(f', 8)
      Note(e', 8)   

   This function is thread-agnostic.

   .. versionchanged:: 1.1.2
      Renamed from ``iterate.backwards( )`` to ``iterate.naive_backward_in( )``.
   '''

   total = 0

   def test(total):
      if start < total:
         if stop is None or total <= stop:
            return True
      return False

   if isinstance(expr, klass):
      #yield expr
      total += 1
      if test(total):
         yield expr
   if isinstance(expr, (list, tuple)):
      for m in reversed(expr):
         for x in naive_backward_in(m, klass):
            #yield x
            total += 1
            if test(total):
               yield x
   if hasattr(expr, '_music'):
      for m in reversed(expr._music):
         for x in naive_backward_in(m, klass):
            #yield x
            total += 1
            if test(total):
               yield x
