from abjad.core.abjadcore import _Abjad


class _SpannerFormatInterface(_Abjad):
   '''Abstract base class. 
      Model format interface for all *Abjad* spanners.'''

   def __init__(self, spanner):
      '''Bind to spanner client.'''
      self._spanner = spanner

   ## PUBLIC ATTRIBUTES ##

   @property
   def spanner(self):
      '''Read-only reference to spanner client.'''
      return self._spanner

   ## PUBLIC METHODS ##

   def _after(self, leaf):
      '''Spanner format contributions to output after leaf.'''
      result = [ ]
      spanner = self.spanner
      if spanner._isMyLastLeaf(leaf):
         result.extend(getattr(spanner, 'reverts', [ ]))
      return result

   def _before(self, leaf):
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

   def report(self, leaves = None):
      '''Print spanner format contributions for every leaf in leaves.'''
      leaves = leaves or self.spanner.leaves
      for leaf in leaves:
         print leaf
         print '\tbefore: %s' % self._before(leaf)
         print '\t after: %s' % self._after(leaf)
         print '\t  left: %s' % self.left(leaf)
         print '\t right: %s' % self.right(leaf)
         print ''

   def right(self, leaf):
      '''Spanner format contributions to output right of leaf.'''
      result = [ ]
      return result
