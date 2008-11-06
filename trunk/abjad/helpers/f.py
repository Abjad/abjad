from abjad.core.component import _Component


def f(expr):
   if isinstance(expr, _Component):
      print expr.format
   elif isinstance(expr, list):
      for x in expr:
         print x.format
   else:
      raise ValueError('must be score component or list.')
