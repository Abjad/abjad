def components_and_grace_containers_forward_in_expr(expr, klass):
   r'''Yield left-to-right `klass` instances in `expr`.
   
   Include grace leaves before main leaves.

   Include grace leaves after main leaves. ::

      abjad> t = Voice(macros.scale(4))
      abjad> Beam(t[:])
      abjad> notes = macros.scale(4, Rational(1, 16))
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

      abjad> for x in iterate.components_and_grace_containers_forward_in_expr(t, Note):
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

   .. versionchanged:: 1.1.2
      renamed ``iterate.grace( )`` to
      ``iterate.components_and_grace_containers_forward_in_expr( )``.
   '''

   if hasattr(expr, 'grace'):
      for m in expr.grace.before:
         for x in components_and_grace_containers_forward_in_expr(m, klass):
            yield x
      if isinstance(expr, klass):
         yield expr
      for m in expr.grace.after:
         for x in components_and_grace_containers_forward_in_expr(m, klass):
            yield x
   elif isinstance(expr, klass):
      yield expr
   if isinstance(expr, (list, tuple)):
      for m in expr:
         for x in components_and_grace_containers_forward_in_expr(m, klass):
            yield x
   if hasattr(expr, '_music'):
      for m in expr._music:
         for x in components_and_grace_containers_forward_in_expr(m, klass):
            yield x
