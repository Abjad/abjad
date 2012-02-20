from abjad.tools.spannertools.Spanner._SpannerFormatInterface import _SpannerFormatInterface


class _HairpinSpannerFormatInterface(_SpannerFormatInterface):

    def __init__(self, spanner):
        _SpannerFormatInterface.__init__(self, spanner)

    ### PUBLIC METHODS ###

    def _right(self, leaf):
        '''Spanner format contribution right of leaf.'''
        from abjad.tools.chordtools.Chord import Chord
        from abjad.tools.notetools.Note import Note
        from abjad.tools import contexttools
        result = []
        spanner = self.spanner
        effective_dynamic = contexttools.get_effective_dynamic(leaf)
        direction_string = ''
        if spanner.direction is not None:
            direction_string = '%s ' % spanner.direction
        if spanner.include_rests:
            if spanner._is_my_first_leaf(leaf):
                result.append('%s\\%s' % (direction_string, spanner.shape_string))
                if spanner.start_dynamic_string:
                    result.append('%s\\%s' % (direction_string, spanner.start_dynamic_string))
            if spanner._is_my_last_leaf(leaf):
                if spanner.stop_dynamic_string:
                    result.append('%s\\%s' % (direction_string, spanner.stop_dynamic_string))
                elif effective_dynamic is None or \
                    effective_dynamic not in \
                    leaf._marks_for_which_component_functions_as_start_component:
                    result.append('\\!')
        else:
            if spanner._is_my_first(leaf, (Chord, Note)):
                result.append('%s\\%s' % (direction_string, spanner.shape_string))
                if spanner.start_dynamic_string:
                    result.append('%s\\%s' % (direction_string, spanner.start_dynamic_string))
            if spanner._is_my_last(leaf, (Chord, Note)):
                if spanner.stop_dynamic_string:
                    result.append('%s\\%s' % (direction_string, spanner.stop_dynamic_string))
                elif effective_dynamic is None:
                    result.append('\\!')
        return result
