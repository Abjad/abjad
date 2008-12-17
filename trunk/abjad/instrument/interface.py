from abjad.spanner.spanner import Spanner


### TODO: turn this into a real interface. Inactive code presently.

class _Instrument(Spanner):

   def __init__(self, long = None, short = None):
      Spanner.__init__(self)
      self.long = long
      self.short = short

   @property
   def default(self):
      if self.long == None and self.short == None:
         return True
      else:
         return False

   def cover(self, *args):
      self.coverHelper('instrument', *args)

   def attach(self, l):
      self.attachHelper('instrument', l)

   def before(self, l):
      result = []
      if self.isAlone(l) or self.isStart(l):
         if self.long:
            result.append(r'\set %s.instrumentName = %s' % (
               l.staff.name, self.long))
         if self.short:
            result.append(r'\set %s.instrumentName = %s' % (
               l.staff.name, self.short))
      return result
