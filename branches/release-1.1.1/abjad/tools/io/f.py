def f(expr):
   '''Print the `LilyPond` input code of `Abjad` expression *expr*.
   
   - *expr* can be any `Abjad` object having a ``format`` property.

   Example::
      
      abjad> t = Staff([Note(1, (1,4)), Rest((1, 8))])
      abjad> f(t)
      \\new Staff {
              cs'4
              r8
      }'''

   print expr.format
