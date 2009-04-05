from abjad.spanner.format import _SpannerFormatInterface


class _BeamSpannerFormatInterface(_SpannerFormatInterface):

   def __init__(self, spanner):
      _SpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   def before(self, leaf):
      '''Spanner format contribution before leaf.'''
      result = [ ]
      result.extend(_SpannerFormatInterface.before(self, leaf))
      return result

   def right(self, leaf):
      '''Spanner format contribution right of leaf.'''
      result = [ ]
      spanner = self.spanner
      if spanner._isMyFirstLeaf(leaf):
         result.append('[')
      if spanner._isMyLastLeaf(leaf):
         result.append(']')   
      return result
