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
   '''Print the LilyPond input code of Abjad expression 'expr'.'''

   print expr.format
