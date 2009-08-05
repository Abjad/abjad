def thread(expr, klass, thread_signature):
   r'''.. versionadded:: 1.1.1

   Yield left-to-right instances of `klass` in `expr` with
   `thread_signature`. ::

      abjad> container = Container(Voice(construct.run(2)) * 2)
      abjad> container.parallel = True
      abjad> container[0].name = 'voice 1'
      abjad> container[1].name = 'vocie 2'
      abjad> staff = Staff(container * 2)
      abjad> pitchtools.diatonicize(staff)
      abjad> print staff.format
      \new Staff {
              <<
                      \context Voice = "voice 1" {
                              c'8
                              d'8
                      }
                      \context Voice = "vocie 2" {
                              e'8
                              f'8
                      }
              >>
              <<
                      \context Voice = "voice 1" {
                              g'8
                              a'8
                      }
                      \context Voice = "vocie 2" {
                              b'8
                              c''8
                      }
              >>
      }

   ::

      abjad> signature = staff.leaves[0].thread.signature
      abjad> for x in iterate.thread(staff, Note, signature):
      ...     x
      ... 
      Note(c', 8)
      Note(d', 8)
      Note(g', 8)
      Note(a', 8)

   The important thing to note is that the function yields only
   those leaves that sit in the same thread.

   Compare with :func:`iterate.naive() <abjad.tools.iterate.naive>`.
   '''

   if isinstance(expr, klass) and expr.thread.signature == thread_signature:
      yield expr
   if isinstance(expr, (list, tuple)):
      for m in expr:
         for x in thread(m, klass, thread_signature):
            yield x
   if hasattr(expr, '_music'):
      for m in expr._music:
         for x in thread(m, klass, thread_signature):
            yield x
