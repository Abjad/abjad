# -*- encoding: utf-8 -*-
import collections
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadObject


class MetricalKernel(AbjadObject):
    r'''A metrical kernel, or offset-impulse-response-filter:

    ::

        >>> hierarchy = timesignaturetools.MetricalHierarchy((5, 8))
        >>> kernel = hierarchy.generate_offset_kernel_to_denominator(8)
        >>> kernel
        MetricalKernel({
            Offset(0, 1): Multiplier(3, 11),
            Offset(1, 8): Multiplier(1, 11),
            Offset(1, 4): Multiplier(1, 11),
            Offset(3, 8): Multiplier(2, 11),
            Offset(1, 2): Multiplier(1, 11),
            Offset(5, 8): Multiplier(3, 11)
        })

    Call the kernel against an expression from which offsets can be counted
    to receive an impulse-response:

    ::

        >>> offsets = [(0, 8), (1, 8), (1, 8), (3, 8)]
        >>> kernel(offsets)
        0.6363636363636364

    Return `MetricalKernel` instance.
    '''
    ### CLASS VARIABLES ###

    __slots__ = (
        '_kernel',
        '_offsets',
        )

    ### INITIALIZER ###

    def __init__(self, kernel):
        assert isinstance(kernel, dict)
        assert 1 < len(kernel)
        for key, value in kernel.iteritems():
            assert isinstance(key, durationtools.Offset)
            assert isinstance(value, durationtools.Multiplier)
        self._kernel = kernel.copy()
        self._offsets = tuple(sorted(self._kernel))

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        offset_count = self.count_offsets_in_expr(expr)
        response = 0.
        for offset, count in offset_count.iteritems():
            if offset in self._kernel:
                response += (self._kernel[offset] * count)
        return float(response)

    def __eq__(self, expr):
        if type(self) == type(expr):
            if self._kernel == expr._kernel:
                return True
        return False

    def __repr__(self):
        result = ['{}({{'.format(self._class_name)]
        offsets = sorted(self._kernel)
        for offset in offsets[:-1]:
            result.append('\t{!r}: {!r},'.format(
                offset, self._kernel[offset]))
        result.append('\t{!r}: {!r}'.format(
            offsets[-1], self._kernel[offsets[-1]]))
        result.append('})')
        return '\n'.join(result)

    ### PUBLIC PROPERTIES ###

    @property
    def kernel(self):
        r'''The kernel datastructure.

        Return dict.
        '''
        return self._kernel.copy()

    ### PUBLIC METHODS ###

    @staticmethod
    def count_offsets_in_expr(expr):
        r'''Count offsets in `expr`.

        Example 1.:

        ::

            >>> score = Score()
            >>> score.append(Staff("c'4. d'8 e'2"))
            >>> score.append(Staff(r'\clef bass c4 b,4 a,2'))

        ..  doctest::

            >>> f(score)
            \new Score <<
                \new Staff {
                    c'4.
                    d'8
                    e'2
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

            >>> MetricalKernel = timesignaturetools.MetricalKernel
            >>> leaves = score.select_leaves()
            >>> counter = MetricalKernel.count_offsets_in_expr(leaves)
            >>> for offset, count in sorted(counter.items()):
            ...     offset, count
            ...
            (Offset(0, 1), 2)
            (Offset(1, 4), 2)
            (Offset(3, 8), 2)
            (Offset(1, 2), 4)
            (Offset(1, 1), 2)

        Example 2.:

        ::

            >>> a = timespantools.Timespan(0, 10)
            >>> b = timespantools.Timespan(5, 15)
            >>> c = timespantools.Timespan(15, 20)

        ::

            >>> counter = MetricalKernel.count_offsets_in_expr((a, b, c))
            >>> for offset, count in sorted(counter.items()):
            ...     offset, count
            ...
            (Offset(0, 1), 1)
            (Offset(5, 1), 1)
            (Offset(10, 1), 1)
            (Offset(15, 1), 2)
            (Offset(20, 1), 1)

        Return counter.
        '''
        counter = collections.Counter()
        for x in expr:
            if hasattr(x, 'start_offset') and hasattr(x, 'stop_offset'):
                counter[x.start_offset] += 1
                counter[x.stop_offset] += 1
            elif hasattr(x, 'timespan'):
                counter[x.get_timespan().start_offset] += 1
                counter[x.get_timespan().stop_offset] += 1
            else:
                offset = durationtools.Offset(x)
                counter[offset] += 1
        return counter
