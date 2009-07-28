from abjad.spanner.format import _SpannerFormatInterface


class _OctavationSpannerFormatInterface(_SpannerFormatInterface):

   def __init__(self, spanner):
      _SpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   ## TODO - test the shit out of the middleCPosition stuff, esp
   ##        clef changes in the middle of an octavation spanner

   def after(self, leaf):
      '''Spanner format contributions after leaf.'''
      result = [ ]
      #result.extend(_GrobHandlerSpanner.after(spanner, leaf))
      result.extend(_SpannerFormatInterface.after(self, leaf))
      spanner = self.spanner
      if spanner._isMyLastLeaf(leaf):
         result.append(r'\ottava #%s' % spanner.stop)
         #result.append(r'#(set-octavation %s)' % spanner.stop)
         #position = leaf.clef.effective.middleCPosition - 7 * spanner.stop
         #result.append(r'\set Staff.middleCPosition = #%s' % position)
      return result

   def _before(self, leaf):
      '''Spanner format contributions before leaf.'''
      result = [ ]
      #result.extend(_GrobHandlerSpanner._before(spanner, leaf))
      result.extend(_SpannerFormatInterface._before(self, leaf))
      spanner = self.spanner
      if spanner._isMyFirstLeaf(leaf):
         result.append(r'\ottava #%s' % spanner.start)
#         result.append(r'#(set-octavation %s)' % spanner.start)
#      if spanner._isMyFirstLeaf(leaf) or leaf.clef.change:
#         position = leaf.clef.effective.middleCPosition - 7 * spanner.start
#         result.append(r'\set Staff.middleCPosition = #%s' % position)
      return result
