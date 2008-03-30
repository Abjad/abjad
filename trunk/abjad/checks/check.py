from re import findall

class _Check(object):

   def __init__(self):
      pass

   def violators(self, expr):
      violators, total = self._run(expr)
      return violators

   def check(self, expr):
      return not self.violators(expr)

   def report(self, expr):
      violators, total = self._run(expr)
      bad = len(violators)
      print '%4d / %4d %s' % (bad, total, self._message)
      
   @property
   def _message(self):
      name = self.__class__.__name__
      parts = findall("[A-Z][a-z]*", name)
      return ' '.join([p.lower() for p in parts])
