from abjad.tools.spannertools.Spanner._SpannerFormatInterface import _SpannerFormatInterface


class _HairpinSpannerFormatInterface(_SpannerFormatInterface):

   def __init__(self, spanner):
      _SpannerFormatInterface.__init__(self, spanner)

   ## PUBLIC METHODS ##

   def _right(self, leaf):
      '''Spanner format contribution right of leaf.'''
      from abjad.components import Chord
      from abjad.components import Note
      from abjad.tools import contexttools
      result = [ ]
      spanner = self.spanner
      effective_dynamic = contexttools.get_effective_dynamic(leaf)
      if not spanner.avoid_rests:
         if spanner._is_my_first_leaf(leaf):
            result.append('\\%s' % spanner._shape)
            if spanner.start:
               result.append('\\%s' % spanner.start)
         if spanner._is_my_last_leaf(leaf):
            if spanner.stop:
               result.append('\\%s' % spanner.stop)
            elif effective_dynamic is None or \
                effective_dynamic not in \
                leaf._marks_for_which_component_functions_as_start_component:
               result.append('\\!')
      else:
         if spanner._is_my_first(leaf, (Chord, Note)):
            result.append('\\%s' % spanner._shape)
            if spanner.start:
               result.append('\\%s' % spanner.start)
         if spanner._is_my_last(leaf, (Chord, Note)):
            if spanner.stop:
               result.append('\\%s' % spanner.stop)
            elif effective_dynamic is None:
               result.append('\\!')
      return result
