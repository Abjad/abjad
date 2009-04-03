from abjad.clef.clef import Clef
from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface


class _ClefInterface(_Interface, _GrobHandler):
   
   def __init__(self, client):
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Clef')
      self._forced = None

   ## PUBLIC ATTRIBUTES ##

   @property
   def change(self):
      client = self._client
      return bool(client._navigator._prevBead and \
         client._navigator._prevBead.clef.name != self.name)

   @property
   def effective(self):
      cur = self._client
      while cur is not None:
         if cur.clef._forced:
            return cur.clef._forced
         else:
            cur = cur._navigator._prevBead
      for x in self._client.parentage.parentage[1:]:
         if hasattr(x, 'clef') and x.clef._forced:
            return x.clef._forced
      return Clef('treble')

   @apply
   def forced( ):
      def fget(self):
         return self._forced
      def fset(self, arg):
         if arg is None:
            self._forced = None
         elif isinstance(arg, str):
            clef = Clef(arg)
            self._forced = clef
         elif isinstance(arg, Clef):
            self._forced = arg
         else:
            raise ValueError('unknown clef specification.')
      return property(**locals( ))

   @property
   def name(self):
      return self.effective.name

   @property
   def opening(self):
      result = [ ]
      result.extend(_GrobHandler.before.fget(self))
      if self.forced or self.change:
         result.append(self.effective.format)
      return result

