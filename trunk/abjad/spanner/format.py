from abjad.core.abjadcore import _Abjad


class _SpannerFormatInterface(_Abjad):

   def __init__(self, spanner):
      self._spanner = spanner

   ## PUBLIC ATTRIBUTES ##

   @property
   def spanner(self):
      return self._spanner

   ## PUBLIC METHODS ##

   def after(self, leaf):
      '''Spanner format contributions to output after leaf.'''
      result = [ ]
      return result

   def before(self, leaf):
      '''Spanner format contributions to output before leaf.'''
      result = [ ]
      return result

   def left(self, leaf):
      '''Spanner format contributions to output left of leaf.'''
      result = [ ]
      return result

   def right(self, leaf):
      '''Spanner format contributions to output right of leaf.'''
      result = [ ]
      return result
