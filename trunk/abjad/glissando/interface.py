from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.spanner.receptor import _SpannerReceptor


class _GlissandoInterface(_Interface, _GrobHandler, _SpannerReceptor):
   '''Handle LilyPond Glissando grob.'''

   def __init__(self, client):
      from abjad.glissando.spanner import Glissando
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Glissando')
      _SpannerReceptor.__init__(self, (Glissando, ))
      self._set = False

   ## OVERLOADS ##

   def __eq__(self, arg):
      assert isinstance(arg, bool)
      return bool(self._set) == arg

   def __nonzero__(self):
      return bool(self._set)

   ## PUBLIC ATTRIBUTES ##

   @property
   def right(self):
      result = [ ]
      if self._set:
         result.append(r'\glissando')
      return result

   @apply
   def set( ):
      def fget(self):
         return self._set
      def fset(self, arg):
         self._set = arg
      return property(**locals( ))

   ## PUBLIC METHODS ##

   def clear(self):
      self._set = None
      _GrobHandler.clear(self)
