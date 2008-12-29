from abjad.clef.clef import _Clef
from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface


class _ClefInterface(_Interface, _GrobHandler):
   
   def __init__(self, client):
      _Interface.__init__(self, client)
      #_GrobHandler.__init__(self, 'Staff.Clef')
      _GrobHandler.__init__(self, 'Clef')
      self._forced = None

   ### PRIVATE ATTRIBUTES ###

   @property
   def _before(self):
      result = [ ]
      result.extend(_GrobHandler._before.fget(self))
      if self.forced or self.change:
         result.append(r'\clef %s' % self.name)
      return result

   ### NOTE: this is kinda kinky:
   ###       reusing _before as _opening;
   ###       reason: Leaf._ClefInterface._before make sense
   ###       analogously as Container._ClefInterface._opening.

   @property
   def _opening(self):
      return self._before

   ### PUBLIC ATTRIBUTES ###

   @property
   def change(self):
      return bool(self._client.prev and \
         self._client.prev.clef.name != self.name)

   @property
   def effective(self):
      cur = self._client
      while cur is not None:
         if cur.clef._forced:
            return cur.clef._forced
         else:
            cur = cur.prev
      #for x in self._client._parentage._parentage:
      #for x in self._client._parentage._iparentage[1:]:
      for x in self._client._parentage._parentage[1:]:
         if hasattr(x, 'clef') and x.clef._forced:
            return x.clef._forced
      return _Clef('treble')

   @apply
   def forced( ):
      def fget(self):
         return self._forced
      def fset(self, arg):
         if arg is None:
            self._forced = None
         elif isinstance(arg, str):
            clef = _Clef(arg)
            self._forced = clef
         elif isinstance(arg, _Clef):
            self._forced = arg
         else:
            raise ValueError('unknown clef specification.')
      return property(**locals( ))

   @property
   def name(self):
      return self.effective.name
