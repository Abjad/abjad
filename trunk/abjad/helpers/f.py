from abjad.component.component import _Component


def f(expr):
   if hasattr(expr, 'format'):
      ### TODO: this case fails for underfull measures ###
      print expr.format
   elif hasattr(expr, '__contains__'):
      for x in expr:
         print x.format
   else:
      raise TypeError(
         'must be format object or be iterable of format objects.')
