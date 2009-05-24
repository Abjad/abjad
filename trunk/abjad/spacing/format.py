from abjad.spanner.format import _SpannerFormatInterface


class _SpacingSpannerFormatInterface(_SpannerFormatInterface):
   '''Create ``SpacingSpanner`` format-time contributions.'''

   def __init__(self, spanner):
      '''Bind to spanner and initialize as type of spanner format interface.'''
      _SpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   def after(self, leaf):
      '''Spanner format contribution after leaf.'''
      result = [ ]
      result.extend(_SpannerFormatInterface.after(self, leaf))
      new_section = self.spanner.new_section
      if new_section:
         if self.spanner._isMyLastLeaf(leaf):
            result.append(r'%%% spacing section ends here %%%')
      return result

   def before(self, leaf):
      '''Spanner format contribution before leaf.'''
      result = [ ]
      new_section = self.spanner.new_section
      if new_section:
         if self.spanner._isMyFirstLeaf(leaf):
            result.append(r'\newSpacingSection')
      result.extend(_SpannerFormatInterface.before(self, leaf))
      return result
