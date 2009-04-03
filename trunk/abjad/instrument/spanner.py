from abjad.spanner.spanner import Spanner


class Instrument(Spanner):

   def __init__(self, music = None, long = None, short = None):
      Spanner.__init__(self, music)
      self.long = long
      self.short = short

   ## PUBLIC ATTRIBUTES ##

   @apply
   def long( ):
      def fget(self):
         return self._long
      def fset(self, arg):
         assert isinstance(arg, str) or arg is None
         self._long = arg
      return property(**locals( ))

   @apply
   def short( ):
      def fget(self):
         return self._short
      def fset(self, arg):
         assert isinstance(arg, str) or arg is None
         self._short = arg
      return property(**locals( ))

   ## PUBLIC METHODS ##

   def after(self, leaf):
      result = [ ]
      result.extend(Spanner.after(self, leaf))
      if self._isMyLastLeaf(leaf):
         #staff = leaf.staff.context
         staff = 'Staff'
         if self.long is not None:
            result.append(r'\unset %s.instrumentName' % staff)
         if self.short is not None:
            result.append(r'\unset %s.shortInstrumentName' % staff)
      return result

   def before(self, leaf):
      result = [ ]
      result.extend(Spanner.before(self, leaf))
      if self._isMyFirstLeaf(leaf):
         #staff = leaf.staff.context
         staff = 'Staff'
         if self.long is not None:
            result.append(r'\set %s.instrumentName = %s' % (
               staff, self.long))
         if self.short is not None:
            result.append(r'\set %s.shortInstrumentName = %s' % (
               staff, self.short))
      return result

