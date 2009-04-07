from abjad.clef.clef import Clef
from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
import types


class _ClefInterface(_Interface, _GrobHandler):
   '''Handle LilyPond Clef grob.
      Interface to find effective clef.
      Interface to force clef changes.'''
   
   def __init__(self, client):
      '''Bind client and LilyPond Clef grob.
         Set forced to None.'''
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Clef')
      self._forced = None

   ## PUBLIC ATTRIBUTES ##

   @property
   def change(self):
      '''True if clef changes here, otherwise False.'''
      #client = self._client
      #return bool(client._navigator._prevBead and \
      #   client._navigator._prevBead.clef.name != self.name)
      return bool(hasattr(self.client, 'prev') and \
         self.client.prev.clef.name != self.name)

   @property
   def effective(self):
      '''Return effective clef or else treble.'''
      #cur = self._client
      cur = self.client
      while cur is not None:
         if cur.clef._forced:
            return cur.clef._forced
         else:
            #cur = cur._navigator._prevBead
            cur = getattr(cur, 'prev', None)
      #for x in self._client.parentage.parentage[1:]:
      for x in self.client.parentage.parentage[1:]:
         if hasattr(x, 'clef') and x.clef._forced:
            return x.clef._forced
      return Clef('treble')

   @apply
   def forced( ):
      '''Forced clef change here.'''
      def fget(self):
         return self._forced
      def fset(self, arg):
         if isinstance(arg, (Clef, types.NoneType)):
            self._forced = arg
         elif isinstance(arg, str):
            self._forced = Clef(arg)
#         if arg is None:
#            self._forced = None
#         elif isinstance(arg, str):
#            clef = Clef(arg)
#            self._forced = clef
#         elif isinstance(arg, Clef):
#            self._forced = arg
         else:
            raise ValueError('unknown clef specification.')
      return property(**locals( ))

   @property
   def name(self):
      '''Name of effective clef as string.'''
      return self.effective.name

   @property
   def opening(self):
      '''Format contribution at container opening or before leaf.'''
      result = [ ]
      #result.extend(_GrobHandler.before.fget(self))
      if self.forced or self.change:
         result.append(self.effective.format)
      return result
