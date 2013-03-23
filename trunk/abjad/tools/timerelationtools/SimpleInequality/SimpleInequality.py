import bisect
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadObject


class SimpleInequality(AbjadObject):
    '''.. versionadded:: 2.12

    Simple inequality.

        >>> template = 'timespan_2.start_offset < timespan_1.start_offset'
        >>> simple_inequality = timerelationtools.SimpleInequality(template)

    ::

        >>> simple_inequality
        SimpleInequality('timespan_2.start_offset < timespan_1.start_offset')

    Return simple inequality.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_template', )

    templates = (
        'offset == timespan.start',
        'offset < timespan.start',
        'offset <= timespan.start',
        'offset == timespan.stop',
        'offset < timespan.stop',
        'offset <= timespan.stop',
        'timespan.start == offset',
        'timespan.start < offset',
        'timespan.start <= offset',
        'timespan.stop == offset',
        'timespan.stop < offset',
        'timespan.stop <= offset',
        'timespan_1.start_offset == timespan_2.start_offset',
        'timespan_1.start_offset < timespan_2.start_offset',
        'timespan_1.start_offset <= timespan_2.start_offset',
        'timespan_1.start_offset == timespan_2.stop_offset',
        'timespan_1.start_offset < timespan_2.stop_offset',
        'timespan_1.start_offset <= timespan_2.stop_offset',
        'timespan_1.stop_offset == timespan_2.start_offset',
        'timespan_1.stop_offset < timespan_2.start_offset',
        'timespan_1.stop_offset <= timespan_2.start_offset',
        'timespan_1.stop_offset == timespan_2.stop_offset',
        'timespan_1.stop_offset < timespan_2.stop_offset',
        'timespan_1.stop_offset <= timespan_2.stop_offset',
        'timespan_2.start_offset == timespan_1.start_offset',
        'timespan_2.start_offset < timespan_1.start_offset',
        'timespan_2.start_offset <= timespan_1.start_offset',
        'timespan_2.start_offset == timespan_1.stop_offset',
        'timespan_2.start_offset < timespan_1.stop_offset',
        'timespan_2.start_offset <= timespan_1.stop_offset',
        'timespan_2.stop_offset == timespan_1.start_offset',
        'timespan_2.stop_offset < timespan_1.start_offset',
        'timespan_2.stop_offset <= timespan_1.start_offset',
        'timespan_2.stop_offset == timespan_1.stop_offset',
        'timespan_2.stop_offset < timespan_1.stop_offset',
        'timespan_2.stop_offset <= timespan_1.stop_offset',
        )

    ### INITIALIZER ###

    def __init__(self, template):
        assert template in self.templates, repr(template)
        self._template = template

    ### PRIVATE METHODS ###

    def _find_index_lt(self, a, x):
        '''Find index of rightmost value less than x.
        '''
        i = bisect.bisect_left(a, x)
        if i:
            return i - 1
        raise ValueError

    def _find_index_le(self, a, x):
        '''Find index of rightmost value less than or equal to x.
        '''
        i = bisect.bisect_right(a, x)
        if i:
            return i - 1
        raise ValueError

    def _find_index_gt(self, a, x):
        '''Find index of leftmost value greater than x.
        '''
        i = bisect.bisect_right(a, x)
        if i != len(a):
            return i
        raise ValueError

    def _find_index_ge(self, a, x):
        '''Find index of leftmost item greater than or equal to x.
        '''
        i = bisect.bisect_left(a, x)
        if i != len(a):
            return i 
        raise ValueError

    # do not indent storage format
    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        return [''.join(
            AbjadObject._get_tools_package_qualified_repr_pieces(self, is_indented=False))]

    def _index(self, a, x):
        '''Find index of leftmost value exactly equal to x.
        '''
        i = bisect.bisect_left(a, x)
        if i != len(a) and a[i] == x:
            return i
        raise ValueError

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def storage_format(self):
        '''Simple inequality storage format.

            >>> z(simple_inequality)
            timerelationtools.SimpleInequality('timespan_2.start_offset < timespan_1.start_offset')

        Return string.
        '''
        return AbjadObject.storage_format.fget(self)

    @property
    def template(self):
        '''Simple inequality template.

            >>> simple_inequality.template
            'timespan_2.start_offset < timespan_1.start_offset'

        Return string.
        '''
        return self._template

    ### PUBLIC METHODS ###

    def evaluate(self, timespan_1_start_offset, timespan_1_stop_offset,
        timespan_2_start_offset, timespan_2_stop_offset):
        template = self.template
        template = template.replace('timespan_1.start_offset', repr(timespan_1_start_offset))
        template = template.replace('timespan_1.stop_offset', repr(timespan_1_stop_offset))
        template = template.replace('timespan_2.start_offset', repr(timespan_2_start_offset))
        template = template.replace('timespan_2.stop_offset', repr(timespan_2_stop_offset))
        truth_value = eval(template, {'Offset': durationtools.Offset})
        return truth_value

    def evaluate_offset_inequality(self, timespan_start, timespan_stop, offset):
        template = self.template
        template = template.replace('timespan.start', repr(timespan_start))
        template = template.replace('timespan.stop', repr(timespan_stop))
        template = template.replace('offset', repr(offset))
        truth_value = eval(template, {'Offset': durationtools.Offset})
        return truth_value

    def get_offset_indices(self, timespan_1, timespan_2_start_offsets, timespan_2_stop_offsets):
        '''Change simple inequality to offset indices.

        .. todo:: add example.

        Return nonnegative integer pair.
        '''

        simple_inequality = self.template
        assert isinstance(simple_inequality, str), repr(simple_inequality)
        leftmost_index, rightmost_index = None, None

        # 1.a
        if simple_inequality == 'timespan_1.start_offset == timespan_2.start_offset':
            try:
                leftmost_index = self._find_index(timespan_2_start_offsets, timespan_1.start_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 1.b
        elif simple_inequality == 'timespan_1.start_offset < timespan_2.start_offset':
            try:
                leftmost_index = self._find_index_gt(timespan_2_start_offsets, timespan_1.start_offset)
                rightmost_index = len(timespan_2_start_offsets)
            except ValueError:
                pass
        # 1.c
        elif simple_inequality == 'timespan_1.start_offset <= timespan_2.start_offset':
            try:
                leftmost_index = self._find_index_ge(timespan_2_start_offsets, timespan_1.start_offset)
                rightmost_index = len(timespan_2_start_offsets)
            except ValueError:
                pass
        # 2.a
        elif simple_inequality == 'timespan_1.start_offset == timespan_2.stop_offset':
            try:
                leftmost_index = self._find_index(timespan_2_stop_offsets, timespan_1.start_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 2.b
        elif simple_inequality == 'timespan_1.start_offset < timespan_2.stop_offset':
            try:
                leftmost_index = self._find_index_gt(timespan_2_stop_offsets, timespan_1.start_offset)
                rightmost_index = len(timespan_2_stop_offsets)
            except ValueError:
                pass
        # 2.c
        elif simple_inequality == 'timespan_1.start_offset <= timespan_2.stop_offset':
            try:
                leftmost_index = self._find_index_ge(timespan_2_stop_offsets, timespan_1.start_offset)
                rightmost_index = len(timespan_2_stop_offsets)
            except ValueError:
                pass
        # 3.a
        elif simple_inequality == 'timespan_1.stop_offset == timespan_2.start_offset':
            try:
                leftmost_index = self._find_index(timespan_2_start_offsets, timespan_1.stop_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 3.b
        elif simple_inequality == 'timespan_1.stop_offset < timespan_2.start_offset':
            try:
                leftmost_index = self._find_index_gt(timespan_2_start_offsets, timespan_1.stop_offset)
                rightmost_index = len(timespan_2_start_offsets)
            except ValueError:
                pass
        # 3.c
        elif simple_inequality == 'timespan_1.stop_offset <= timespan_2.start_offset':
            try:
                leftmost_index = self._find_index_ge(timespan_2_start_offsets, timespan_1.stop_offset)
                rightmost_index = len(timespan_2_start_offsets)
            except ValueError:
                pass
        # 4.a
        elif simple_inequality == 'timespan_1.stop_offset == timespan_2.stop_offset':
            try:
                leftmost_index = self._find_index(timespan_2_start_offsets, timespan_1.stop_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 4.b
        elif simple_inequality == 'timespan_1.stop_offset < timespan_2.stop_offset':
            try:
                leftmost_index = self._find_index_gt(timespan_2_stop_offsets, timespan_1.stop_offset)
                rightmost_index = len(timespan_2_stop_offsets)
            except ValueError:
                pass
        # 4.c
        elif simple_inequality == 'timespan_1.stop_offset <= timespan_2.stop_offset':
            try:
                leftmost_index = self._find_index_ge(timespan_2_stop_offsets, timespan_1.stop_offset)
                rightmost_index = len(timespan_2_stop_offsets)
            except ValueError:
                pass
        # 5.a
        elif simple_inequality == 'timespan_2.start_offset == timespan_1.start_offset':
            try:
                leftmost_index = self._find_index(timespan_2_start_offsets, timespan_1.start_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 5.b
        elif simple_inequality == 'timespan_2.start_offset < timespan_1.start_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_ge(timespan_2_start_offsets, timespan_1.start_offset)
            except ValueError:
                pass
        # 5.c
        elif simple_inequality == 'timespan_2.start_offset <= timespan_1.start_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_gt(timespan_2_start_offsets, timespan_1.start_offset)
            except ValueError:
                pass
        # 6.a
        elif simple_inequality == 'timespan_2.start_offset == timespan_1.stop_offset':
            try:
                leftmost_index = self._find_index(timespan_2_start_offsets, timespan_1.stop_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 6.b 
        elif simple_inequality == 'timespan_2.start_offset < timespan_1.stop_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_ge(timespan_2_start_offsets, timespan_1.stop_offset)
            except ValueError:
                pass
        # 6.c 
        elif simple_inequality == 'timespan_2.start_offset <= timespan_1.stop_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_gt(timespan_2_start_offsets, timespan_1.stop_offset)
            except ValueError:
                pass
        # 7.a
        elif simple_inequality == 'timespan_2.stop_offset == timespan_1.start_offset':
            try:
                leftmost_index = self._find_index(timespan_2_stop_offsets, timespan_1.start_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 7.b
        elif simple_inequality == 'timespan_2.stop_offset < timespan_1.start_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_ge(timespan_2_stop_offsets, timespan_1.start_offset)
            except ValueError:
                pass
        # 7.c
        elif simple_inequality == 'timespan_2.stop_offset <= timespan_1.start_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_gt(timespan_2_stop_offsets, timespan_1.start_offset)
            except ValueError:
                pass
        # 8.a
        elif simple_inequality == 'timespan_2.stop_offset == timespan_1.stop_offset':
            try:
                leftmost_index = self._find_index(timespan_2_stop_offsets, timespan_1.stop_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 8.b
        elif simple_inequality == 'timespan_2.stop_offset < timespan_1.stop_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_ge(timespan_2_stop_offsets, timespan_1.stop_offset)
            except ValueError:
                pass
        # 8.c
        elif simple_inequality == 'timespan_2.stop_offset <= timespan_1.stop_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_gt(timespan_2_stop_offsets, timespan_1.stop_offset)
            except ValueError:
                pass
        else:
            raise ValueError(simple_inequality)

        if leftmost_index is not None and rightmost_index is not None:
            return leftmost_index, rightmost_index
        else:
            return []
