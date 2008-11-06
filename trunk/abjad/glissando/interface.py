from abjad.core.attributeformatter import _AttributeFormatter
from abjad.core.interface import _Interface
from abjad.core.spannerreceptor import _SpannerReceptor


class _GlissandoInterface(_Interface, _AttributeFormatter, _SpannerReceptor):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _AttributeFormatter.__init__(self, 'Glissando')
      _SpannerReceptor.__init__(self, ['Glissando'])
      self._set = None

   ### OVERLOADS ###

   def __eq__(self, arg):
      assert isinstance(arg, bool)
      return bool(self._set) == arg

   def __nonzero__(self):
      return bool(self._set)

   ### PRIVATE ATTRIBUTES ###

   @property
   def _right(self):
      result = [ ]
      if self._set:
         result.append(r'\glissando')
      return result

   ### PUBLIC METHODS ###

   def clear(self):
      self._set = None
      _AttributeFormatter.clear(self)

