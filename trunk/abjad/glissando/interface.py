from abjad.core.grobhandler import _GrobHandler
from abjad.core.interface import _Interface
from abjad.spanner.receptor import _SpannerReceptor


class _GlissandoInterface(_Interface, _GrobHandler, _SpannerReceptor):

   def __init__(self, client):
      from abjad.glissando.spanner import Glissando
      _Interface.__init__(self, client)
      _GrobHandler.__init__(self, 'Glissando')
      #_SpannerReceptor.__init__(self, ['Glissando'])
      _SpannerReceptor.__init__(self, (Glissando, ))
      self._set = None

   ## OVERLOADS ##

   def __eq__(self, arg):
      assert isinstance(arg, bool)
      return bool(self._set) == arg

   def __nonzero__(self):
      return bool(self._set)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _right(self):
      result = [ ]
      if self._set:
         result.append(r'\glissando')
      return result

   ## PUBLIC METHODS ##

   def clear(self):
      self._set = None
      _GrobHandler.clear(self)
