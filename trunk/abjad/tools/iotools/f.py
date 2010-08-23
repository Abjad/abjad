def f(expr):
   r'''Print the LilyPond input code of `expr`.
   
   ::
      
      abjad> t = Staff([Note(1, (1,4)), Rest((1, 8))])
      abjad> f(t)
      \new Staff {
              cs'4
              r8
      }
   '''

   print expr.format
