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
      spanner = self.spanner
      if spanner._isMyLastLeaf(leaf):
         result.extend(getattr(spanner, 'reverts', [ ]))
      return result

   def before(self, leaf):
      '''Spanner format contributions to output before leaf.'''
      result = [ ]
      spanner = self.spanner
      if spanner._isMyFirstLeaf(leaf):
         result.extend(getattr(spanner, 'overrides', [ ]))
      return result

   def left(self, leaf):
      '''Spanner format contributions to output left of leaf.'''
      result = [ ]
      return result

   def right(self, leaf):
      '''Spanner format contributions to output right of leaf.'''
      result = [ ]
      return result
