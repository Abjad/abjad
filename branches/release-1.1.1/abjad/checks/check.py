from abjad.core.abjadcore import _Abjad
from re import findall


class _Check(_Abjad):

   def __init__(self):
      pass

   ## PRIVATE ATTRIBUTES ##

   @property
   def _message(self):
      name = self.__class__.__name__
      parts = findall("[A-Z][a-z]*", name)
      return ' '.join([p.lower( ) for p in parts])

   ## PUBLIC ATTRIBUTES ##

   def check(self, expr):
      return not self.violators(expr)

   def report(self, expr):
      violators, total = self._run(expr)
      bad = len(violators)
      print '%4d / %4d %s' % (bad, total, self._message)
      
   def violators(self, expr):
      violators, total = self._run(expr)
      return violators
