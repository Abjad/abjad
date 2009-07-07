from abjad.component.component import _Component


def backwards(expr, klass = _Component):
   r'''Yield right-to-left instances of `klass` in `expr`.

   ::

      abjad> staff = Staff(FixedDurationTuplet((2, 8), construct.run(3)) * 2)
      abjad> pitchtools.diatonicize(staff)
      abjad> print staff.format
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

   ::

      abjad> for x in iterate.backwards(staff, Note):
      ...     x 
      ... 
      Note(a', 8)
      Note(g', 8)
      Note(f', 8)
      Note(e', 8)
      Note(d', 8)
      Note(c', 8)

   ::

      abjad> for x in iterate.backwards(staff, FixedDurationTuplet):
      ...     x
      ... 
      FixedDurationTuplet(1/4, [f'8, g'8, a'8])
      FixedDurationTuplet(1/4, [c'8, d'8, e'8])

   .. note:: This naive iteration ignores threads.
   '''

   if isinstance(expr, klass):
      yield expr
   if isinstance(expr, (list, tuple)):
      for m in reversed(expr):
         for x in backwards(m, klass):
            yield x
   if hasattr(expr, '_music'):
      for m in reversed(expr._music):
         for x in backwards(m, klass):
            yield x
