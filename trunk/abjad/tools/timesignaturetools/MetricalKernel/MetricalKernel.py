from abjad.tools import durationtools
from abjad.tools.abctools import AbjadObject


class MetricalKernel(AbjadObject):
    '''A metrical kernel, or offset-impulse-response-filter:

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
    ### CLASS ATTRIBUTES ###

    __slots__ = ('_kernel', '_offsets')

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
        offset_count = durationtools.count_offsets_in_expr(expr)
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
            result.append('\t{!r}: {!r},'.format(offset, self._kernel[offset]))
        result.append('\t{!r}: {!r}'.format(offsets[-1], self._kernel[offsets[-1]]))
        result.append('})')
        return '\n'.join(result)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def kernel(self):
        '''The kernel datastructure.

        Return dict.
        '''
        return self._kernel.copy()

