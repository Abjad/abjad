from abjad.spanners.Spanner.format import _SpannerFormatInterface


class _HairpinSpannerFormatInterface(_SpannerFormatInterface):

   def __init__(self, spanner):
      _SpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   def _right(self, leaf):
      '''Spanner format contribution right of leaf.'''
      from abjad.components.Chord import Chord
      from abjad.components.Note import Note
      result = [ ]
      spanner = self.spanner
      if not spanner.trim:
         if spanner._is_my_first_leaf(leaf):
            result.append('\\%s' % spanner._shape)
            if spanner.start:
               result.append('\\%s' % spanner.start)
         if spanner._is_my_last_leaf(leaf):
            if spanner.stop:
               result.append('\\%s' % spanner.stop)
            elif not leaf.dynamics.mark:
               result.append('\\!')
      else:
         if spanner._is_my_first(leaf, (Chord, Note)):
            result.append('\\%s' % spanner._shape)
            if spanner.start:
               result.append('\\%s' % spanner.start)
         if spanner._is_my_last(leaf, (Chord, Note)):
            if spanner.stop:
               result.append('\\%s' % spanner.stop)
            elif not leaf.dynamics.mark:
               result.append('\\!')
      return result
