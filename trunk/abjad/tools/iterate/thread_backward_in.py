def thread_backward_in(expr, klass, thread_signature):
   r'''.. versionadded:: 1.1.2

   Yield right-to-left instances of `klass` in `expr` with
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

      abjad> signature = staff.leaves[-1].thread.signature
      abjad> for x in iterate.thread_backward_in(staff, Note, signature):
      ...     x
      ... 
      Note(c'', 8)
      Note(b', 8)
      Note(f', 8)
      Note(e', 8)

   The important thing to note is that the function yields only
   those leaves that sit in the same thread.

   Compare with :func:`iterate.naive_backward_in() 
   <abjad.tools.iterate.naive_backward>`.
   '''

   if isinstance(expr, klass) and expr.thread.signature == thread_signature:
      yield expr
   if isinstance(expr, (list, tuple)):
      for m in reversed(expr):
         for x in thread_backward_in(m, klass, thread_signature):
            yield x
   if hasattr(expr, '_music'):
      for m in reversed(expr._music):
         for x in thread_backward_in(m, klass, thread_signature):
            yield x
