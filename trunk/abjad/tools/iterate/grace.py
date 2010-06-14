def grace(expr, klass):
   r'''Yield left-to-right `klass` instances in `expr`.
   
   Include grace leaves before main leaves.

   Include grace leaves after main leaves. ::

      abjad> t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> Beam(t[:])
      abjad> notes = leaftools.make_first_n_notes_in_ascending_diatonic_scale(4, Rational(1, 16))
      abjad> t[1].grace.before.extend(notes[:2])
      abjad> t[1].grace.after.extend(notes[2:])
      abjad> print t.format
      \new Voice {
              c'8 [
              \grace {
                      c'16
                      d'16
              }
              \afterGrace
              d'8
              {
                      e'16
                      f'16
              }
              e'8
              f'8 ]
      }

   ::

      abjad> for x in iterate.grace(t, Note):
      ...     x
      ... 
      Note(c', 8)
      Note(c', 16)
      Note(d', 16)
      Note(d', 8)
      Note(e', 16)
      Note(f', 16)
      Note(e', 8)
      Note(f', 8)

   .. note:: This naive iteration ignores threads.
   '''

   if hasattr(expr, 'grace'):
      for m in expr.grace.before:
         for x in grace(m, klass):
            yield x
      if isinstance(expr, klass):
         yield expr
      for m in expr.grace.after:
         for x in grace(m, klass):
            yield x
   elif isinstance(expr, klass):
      yield expr
   if isinstance(expr, (list, tuple)):
      for m in expr:
         for x in grace(m, klass):
            yield x
   if hasattr(expr, '_music'):
      for m in expr._music:
         for x in grace(m, klass):
            yield x
