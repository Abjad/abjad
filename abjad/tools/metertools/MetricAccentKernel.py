# -*- coding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import systemtools
from abjad.tools.abctools import AbjadValueObject


class MetricAccentKernel(AbjadValueObject):
    r'''A metric accent kernel.

    ..  container:: example

        ::

            >>> hierarchy = metertools.Meter((7, 8))
            >>> kernel = hierarchy.generate_offset_kernel_to_denominator(8)
            >>> kernel
            MetricAccentKernel(
                {
                    Offset(0, 1): Multiplier(3, 14),
                    Offset(1, 8): Multiplier(1, 14),
                    Offset(1, 4): Multiplier(1, 14),
                    Offset(3, 8): Multiplier(1, 7),
                    Offset(1, 2): Multiplier(1, 14),
                    Offset(5, 8): Multiplier(1, 7),
                    Offset(3, 4): Multiplier(1, 14),
                    Offset(7, 8): Multiplier(3, 14),
                    }
                )

    Call the kernel against an expression from which offsets can be counted
    to receive an impulse-response:

    ..  container:: example

        ::

            >>> offsets = [(0, 8), (1, 8), (1, 8), (3, 8)]
            >>> kernel(offsets)
            Multiplier(1, 2)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_kernel',
        '_offsets',
        )

    ### INITIALIZER ###

    def __init__(self, kernel=None):
        kernel = kernel or {}
        assert isinstance(kernel, dict)
        #assert 1 < len(kernel)
        for key, value in kernel.items():
            assert isinstance(key, durationtools.Offset)
            assert isinstance(value, durationtools.Multiplier)
        self._kernel = kernel.copy()
        self._offsets = tuple(sorted(self._kernel))

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls metrical accent kernal on `expr`.

        ::

            >>> upper_staff = Staff("c'8 d'4. e'8 f'4.")
            >>> lower_staff = Staff(r'\clef bass c4 b,4 a,2')
            >>> score = Score([upper_staff, lower_staff])

        ::

            >>> kernel = metertools.MetricAccentKernel.from_meter((4, 4))
            >>> kernel(score)
            Multiplier(10, 33)

        Returns float.
        '''
        offset_count = self.count_offsets_in_expr(expr)
        response = durationtools.Multiplier(0, 1)
        for offset, count in offset_count.items():
            if offset in self._kernel:
                weight = self._kernel[offset]
                weighted_count = weight * count
                response += weighted_count
        return response

    def __eq__(self, expr):
        r'''Is true when `expr` is a metrical accent kernal with a kernal equal
        to that of this metrical accent kernel. Otherwise false.

        Returns true or false.
        '''
        if type(self) == type(expr):
            if self._kernel == expr._kernel:
                return True
        return False

    def __hash__(self):
        r'''Hashes metric accent kernel.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(MetricAccentKernel, self).__hash__()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=True,
            storage_format_args_values=[self.kernel],
            storage_format_kwargs_names=[],
            )

    ### PUBLIC METHODS ###

    @staticmethod
    def count_offsets_in_expr(expr):
        r'''Count offsets in `expr`.

        ..  container:: example

            **Example 1:**

            ::

                >>> upper_staff = Staff("c'8 d'4. e'8 f'4.")
                >>> lower_staff = Staff(r'\clef bass c4 b,4 a,2')
                >>> score = Score([upper_staff, lower_staff])

            ..  doctest::

                >>> print(format(score))
                \new Score <<
                    \new Staff {
                        c'8
                        d'4.
                        e'8
                        f'4.
                    }
                    \new Staff {
                        \clef "bass"
                        c4
                        b,4
                        a,2
                    }
                >>

            ::

                >>> show(score) # doctest: +SKIP

            ::

                >>> MetricAccentKernel = metertools.MetricAccentKernel
                >>> selector = select().by_leaf(flatten=True)
                >>> leaves = selector(score)
                >>> counter = MetricAccentKernel.count_offsets_in_expr(leaves)
                >>> for offset, count in sorted(counter.items()):
                ...     offset, count
                ...
                (Offset(0, 1), 2)
                (Offset(1, 8), 2)
                (Offset(1, 4), 2)
                (Offset(1, 2), 4)
                (Offset(5, 8), 2)
                (Offset(1, 1), 2)

        ..  container:: example

            **Example 2:**

            ::

                >>> a = timespantools.Timespan(0, 10)
                >>> b = timespantools.Timespan(5, 15)
                >>> c = timespantools.Timespan(15, 20)

            ::

                >>> counter = MetricAccentKernel.count_offsets_in_expr((a, b, c))
                >>> for offset, count in sorted(counter.items()):
                ...     offset, count
                ...
                (Offset(0, 1), 1)
                (Offset(5, 1), 1)
                (Offset(10, 1), 1)
                (Offset(15, 1), 2)
                (Offset(20, 1), 1)

        Returns counter.
        '''
        from abjad.tools import metertools
        return metertools.OffsetCounter(expr)

    @staticmethod
    def from_meter(meter, denominator=32, normalize=True):
        r'''Create a metric accent kernel from `meter`.

        Returns new metric accent kernel.
        '''
        from abjad.tools import metertools
        if not isinstance(meter, metertools.Meter):
            meter = metertools.Meter(meter)
        return meter.generate_offset_kernel_to_denominator(
            denominator=denominator,
            normalize=normalize,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        r'''Gets duration.
        '''
        return durationtools.Duration(self._offsets[-1])

    @property
    def kernel(self):
        r'''The kernel datastructure.

        Returns dict.
        '''
        return self._kernel.copy()
