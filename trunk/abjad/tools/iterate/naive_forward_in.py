from abjad.leaf import _Leaf


def naive_forward_in(expr, klass = _Leaf, start = 0, stop = None):
   r'''Yield left-to-right instances of `klass` in `expr`. ::

      abjad> container = Container(Voice(construct.run(2)) * 2)
      abjad> container.parallel = True
      abjad> container[0].name = 'voice 1'
      abjad> container[1].name = 'vocie 2'
      abjad> staff = Staff(container * 2)
      abjad> pitchtools.diatonicize(staff)
      abjad> f(staff)
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
      abjad> for x in iterate.naive_forward_in(staff, Note):
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
   
   .. versionadded:: 1.1.2
      optional `start` and `stop` keyword parameters.

   ::

      abjad> for x in iterate.naive_forward_in(staff, Note, start = 0, stop = 4):
      ...     x
      ... 
      Note(c', 8)
      Note(d', 8)
      Note(e', 8)
      Note(f', 8)

   ::

      abjad> for x in iterate.naive_forward_in(staff, Note, start = 4):
      ...     x
      ... 
      Note(g', 8)
      Note(a', 8)
      Note(b', 8)
      Note(c'', 8)

   ::

      abjad> for x in iterate.naive_forward_in(staff, Note, start = 4, stop = 6):
      ...     x
      ... 
      Note(g', 8)
      Note(a', 8)   

   This function is thread-agnostic.

   .. versionchanged:: 1.1.2
      Renamed from ``iterate.naive( )`` to ``iterate.naive_forward_in( )``.

   .. versionchanged:: 1.1.2
      `klass` now defaults to ``_Leaf``.
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
      for m in expr:
         for x in naive_forward_in(m, klass):
            #yield x
            total += 1
            if test(total):
               yield x
   if hasattr(expr, '_music'):
      for m in expr._music:
         for x in naive_forward_in(m, klass):
            #yield x
            total += 1
            if test(total):
               yield x
