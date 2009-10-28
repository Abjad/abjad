def naive_forward(expr, klass):
   r'''.. versionchanged:: 1.1.2
      Renamed from ``iterate.naive`` to ``iterate.naive_forward``.

   Yield left-to-right instances of `klass` in `expr`.

   Treat `expr` as an undifferentiated tree; ignore threads. ::

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

      abjad> for x in iterate.naive_forward(staff, Note):
      ...     x
      ... 
      Note(c', 8)
      Note(d', 8)
      Note(e', 8)
      Note(f', 8)
      Note(g', 8)
      Note(a', 8)
      Note(b', 8)
      Note(c'', 8)
   
   The important thing to notice here is that the function yields
   notes with no regard for the threads in the which the notes appear.

   Compare with :func:`iterate.thread() <abjad.tools.iterate.thread>`.
   '''

   if isinstance(expr, klass):
      yield expr
   if isinstance(expr, (list, tuple)):
      for m in expr:
         for x in naive_forward(m, klass):
            yield x
   if hasattr(expr, '_music'):
      for m in expr._music:
         for x in naive_forward(m, klass):
            yield x
