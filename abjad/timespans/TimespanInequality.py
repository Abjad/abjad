import bisect
from abjad import system
from abjad.system.AbjadObject import AbjadObject


class TimespanInequality(AbjadObject):
    """
    Timespan inequality.

    ..  container:: example

        >>> template = 'timespan_2.start_offset < timespan_1.start_offset'
        >>> inequality = abjad.TimespanInequality(template)

        >>> inequality
        TimespanInequality('timespan_2.start_offset < timespan_1.start_offset')

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Time relations'

    __slots__ = (
        '_template',
        )

    _publish_storage_format = True

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

    def __init__(self, template=None):
        template = template or \
            'timespan_1.start_offset < timespan_2.start_offset'
        assert template in self.templates, repr(template)
        self._template = template

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        """
        Formats inequality.

            >>> template = 'timespan_2.start_offset < timespan_1.start_offset'
            >>> inequality = abjad.TimespanInequality(template)
            >>> abjad.f(inequality)
            abjad.TimespanInequality('timespan_2.start_offset < timespan_1.start_offset')

        Returns string.
        """
        if format_specification in ('', 'storage'):
            return system.StorageFormatManager(self).get_storage_format()
        return str(self)

    ### PRIVATE METHODS ###

    def _find_index_ge(self, a, x):
        """
        Finds index of leftmost item greater than or equal to x.
        """
        i = bisect.bisect_left(a, x)
        if i != len(a):
            return i
        raise ValueError

    def _find_index_gt(self, a, x):
        """
        Finds index of leftmost value greater than x.
        """
        i = bisect.bisect_right(a, x)
        if i != len(a):
            return i
        raise ValueError

    def _find_index_le(self, a, x):
        """
        Finds index of rightmost value less than or equal to x.
        """
        i = bisect.bisect_right(a, x)
        if i:
            return i - 1
        raise ValueError

    def _find_index_lt(self, a, x):
        """
        Finds index of rightmost value less than x.
        """
        i = bisect.bisect_left(a, x)
        if i:
            return i - 1
        raise ValueError

    def _get_format_specification(self):
        return system.FormatSpecification(
            client=self,
            storage_format_args_values=[self.template],
            storage_format_is_indented=False,
            storage_format_kwargs_names=[],
            )

    def _index(self, a, x):
        """
        Finds index of leftmost value exactly equal to x.
        """
        i = bisect.bisect_left(a, x)
        if i != len(a) and a[i] == x:
            return i
        raise ValueError

    @staticmethod
    def _make_repr(offset):
        return 'Offset({}, {})'.format(*offset.pair)

    ### PUBLIC METHODS ###

    def evaluate(
        self,
        timespan_1_start_offset,
        timespan_1_stop_offset,
        timespan_2_start_offset,
        timespan_2_stop_offset,
        ):
        """
        Evalutes inequality.

        Returns true or false.
        """
        import abjad
        make_repr = self._make_repr
        template = self.template
        template = template.replace(
            'timespan_1.start_offset', make_repr(timespan_1_start_offset))
        template = template.replace(
            'timespan_1.stop_offset', make_repr(timespan_1_stop_offset))
        template = template.replace(
            'timespan_2.start_offset', make_repr(timespan_2_start_offset))
        template = template.replace(
            'timespan_2.stop_offset', make_repr(timespan_2_stop_offset))
        truth_value = eval(template, {'Offset': abjad.Offset})
        return truth_value

    def evaluate_offset_inequality(
        self,
        timespan_start,
        timespan_stop,
        offset,
        ):
        """
        Evalutes offset inequality.

        Returns true or false.
        """
        import abjad
        make_repr = self._make_repr
        template = self.template
        template = self.template
        template = template.replace(
            'timespan.start', make_repr(timespan_start))
        template = template.replace(
            'timespan.stop', make_repr(timespan_stop))
        template = template.replace(
            'offset', make_repr(offset))
        truth_value = eval(template, {'Offset': abjad.Offset})
        return truth_value

    def get_offset_indices(
        self,
        timespan_1,
        timespan_2_start_offsets,
        timespan_2_stop_offsets,
        ):
        """
        Gets offset indices of inequality.

        .. todo:: add example.

        Returns nonnegative integer pair.
        """
        inequality = self.template
        assert isinstance(inequality, str), repr(inequality)
        leftmost_index, rightmost_index = None, None

        # 1.a
        if inequality == \
            'timespan_1.start_offset == timespan_2.start_offset':
            try:
                leftmost_index = self._find_index(
                    timespan_2_start_offsets, timespan_1.start_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 1.b
        elif inequality == \
            'timespan_1.start_offset < timespan_2.start_offset':
            try:
                leftmost_index = self._find_index_gt(
                    timespan_2_start_offsets, timespan_1.start_offset)
                rightmost_index = len(timespan_2_start_offsets)
            except ValueError:
                pass
        # 1.c
        elif inequality == \
            'timespan_1.start_offset <= timespan_2.start_offset':
            try:
                leftmost_index = self._find_index_ge(
                    timespan_2_start_offsets, timespan_1.start_offset)
                rightmost_index = len(timespan_2_start_offsets)
            except ValueError:
                pass
        # 2.a
        elif inequality == \
            'timespan_1.start_offset == timespan_2.stop_offset':
            try:
                leftmost_index = self._find_index(
                    timespan_2_stop_offsets, timespan_1.start_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 2.b
        elif inequality == \
            'timespan_1.start_offset < timespan_2.stop_offset':
            try:
                leftmost_index = self._find_index_gt(
                    timespan_2_stop_offsets, timespan_1.start_offset)
                rightmost_index = len(timespan_2_stop_offsets)
            except ValueError:
                pass
        # 2.c
        elif inequality == \
            'timespan_1.start_offset <= timespan_2.stop_offset':
            try:
                leftmost_index = self._find_index_ge(
                    timespan_2_stop_offsets, timespan_1.start_offset)
                rightmost_index = len(timespan_2_stop_offsets)
            except ValueError:
                pass
        # 3.a
        elif inequality == \
            'timespan_1.stop_offset == timespan_2.start_offset':
            try:
                leftmost_index = self._find_index(
                    timespan_2_start_offsets, timespan_1.stop_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 3.b
        elif inequality == \
            'timespan_1.stop_offset < timespan_2.start_offset':
            try:
                leftmost_index = self._find_index_gt(
                    timespan_2_start_offsets, timespan_1.stop_offset)
                rightmost_index = len(timespan_2_start_offsets)
            except ValueError:
                pass
        # 3.c
        elif inequality == \
            'timespan_1.stop_offset <= timespan_2.start_offset':
            try:
                leftmost_index = self._find_index_ge(
                    timespan_2_start_offsets, timespan_1.stop_offset)
                rightmost_index = len(timespan_2_start_offsets)
            except ValueError:
                pass
        # 4.a
        elif inequality == \
            'timespan_1.stop_offset == timespan_2.stop_offset':
            try:
                leftmost_index = self._find_index(
                    timespan_2_start_offsets, timespan_1.stop_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 4.b
        elif inequality == \
            'timespan_1.stop_offset < timespan_2.stop_offset':
            try:
                leftmost_index = self._find_index_gt(
                    timespan_2_stop_offsets, timespan_1.stop_offset)
                rightmost_index = len(timespan_2_stop_offsets)
            except ValueError:
                pass
        # 4.c
        elif inequality == \
            'timespan_1.stop_offset <= timespan_2.stop_offset':
            try:
                leftmost_index = self._find_index_ge(
                    timespan_2_stop_offsets, timespan_1.stop_offset)
                rightmost_index = len(timespan_2_stop_offsets)
            except ValueError:
                pass
        # 5.a
        elif inequality == \
            'timespan_2.start_offset == timespan_1.start_offset':
            try:
                leftmost_index = self._find_index(
                    timespan_2_start_offsets, timespan_1.start_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 5.b
        elif inequality == \
            'timespan_2.start_offset < timespan_1.start_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_ge(
                    timespan_2_start_offsets, timespan_1.start_offset)
            except ValueError:
                pass
        # 5.c
        elif inequality == \
            'timespan_2.start_offset <= timespan_1.start_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_gt(
                    timespan_2_start_offsets, timespan_1.start_offset)
            except ValueError:
                pass
        # 6.a
        elif inequality == \
            'timespan_2.start_offset == timespan_1.stop_offset':
            try:
                leftmost_index = self._find_index(
                    timespan_2_start_offsets, timespan_1.stop_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 6.b
        elif inequality == \
            'timespan_2.start_offset < timespan_1.stop_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_ge(
                    timespan_2_start_offsets, timespan_1.stop_offset)
            except ValueError:
                pass
        # 6.c
        elif inequality == \
            'timespan_2.start_offset <= timespan_1.stop_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_gt(
                    timespan_2_start_offsets, timespan_1.stop_offset)
            except ValueError:
                pass
        # 7.a
        elif inequality == \
            'timespan_2.stop_offset == timespan_1.start_offset':
            try:
                leftmost_index = self._find_index(
                    timespan_2_stop_offsets, timespan_1.start_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 7.b
        elif inequality == \
            'timespan_2.stop_offset < timespan_1.start_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_ge(
                    timespan_2_stop_offsets, timespan_1.start_offset)
            except ValueError:
                pass
        # 7.c
        elif inequality == \
            'timespan_2.stop_offset <= timespan_1.start_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_gt(
                    timespan_2_stop_offsets, timespan_1.start_offset)
            except ValueError:
                pass
        # 8.a
        elif inequality == \
            'timespan_2.stop_offset == timespan_1.stop_offset':
            try:
                leftmost_index = self._find_index(
                    timespan_2_stop_offsets, timespan_1.stop_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 8.b
        elif inequality == \
            'timespan_2.stop_offset < timespan_1.stop_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_ge(
                    timespan_2_stop_offsets, timespan_1.stop_offset)
            except ValueError:
                pass
        # 8.c
        elif inequality == \
            'timespan_2.stop_offset <= timespan_1.stop_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_gt(
                    timespan_2_stop_offsets, timespan_1.stop_offset)
            except ValueError:
                pass
        else:
            raise ValueError(inequality)

        if leftmost_index is not None and rightmost_index is not None:
            return leftmost_index, rightmost_index
        else:
            return []

    ### PUBLIC PROPERTIES ###

    @property
    def template(self):
        """
        Gets template of inequality.

            >>> template = 'timespan_2.start_offset < timespan_1.start_offset'
            >>> inequality = abjad.TimespanInequality(template)
            >>> inequality.template
            'timespan_2.start_offset < timespan_1.start_offset'

        Returns string.
        """
        return self._template
