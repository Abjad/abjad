#def f(expr):
#   if hasattr(expr, 'format'):
#      print expr.format
#   elif hasattr(expr, '__contains__'):
#      for x in expr:
#         print x.format
#   else:
#      raise TypeError(
#         'must be format object or be iterable of format objects.')

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
