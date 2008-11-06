from abjad.core.attributeformatter import _AttributeFormatter
from abjad.core.interface import _Interface
from abjad.core.spannerreceptor import _SpannerReceptor


class _TieInterface(_Interface, _AttributeFormatter, _SpannerReceptor):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _AttributeFormatter.__init__(self, 'Tie')
      _SpannerReceptor.__init__(self, ['Tie'])
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
         result.append(r'~')
      return result

   ### PUBLIC ATTRIBUTES ###

   ### TODO generalize these to work with Glissando?
   @property
   def head(self):
      '''True if self.first or self.tie and not self.prev.tie'''
      if self.first or (self._set and not self.tied):
         return True
      else:
         return False

   @property
   def tied(self):
      '''True if the previous leaf has a leaf tie.'''
      if self._client.prev and self._client.prev.tie:
         return True
      else:
         return False

   @property
   def tail(self):
      '''True if self.tied and not self.tie or self.last.'''
      if self.last or (self.tied and not self._set):
         return True
      else:
         return False
         
   ### PUBLIC METHODS ###

   def clear(self):
      self._set = None
      _AttributeFormatter.clear(self)
