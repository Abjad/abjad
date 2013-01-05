import bisect
import numbers
import operator
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadObject


class BreakPointFunction(AbjadObject):
    '''A break-point function:

    ::

        >>> from experimental.tools import breakpointtools

    ::

        >>> bpf = breakpointtools.BreakPointFunction({
        ...     0.:   0.,
        ...     0.75: (-1, 1.),
        ...     1.:   0.25,
        ... })

    Allows interpolated lookup, and supports discontiguities on the y-axis:

    ::

        >>> for x in (-0.5, 0., 0.25, 0.5, 0.7499, 0.75, 1., 1.5):
        ...     bpf[x]
        0.0
        0.0
        -0.3333333333333333
        -0.6666666666666666
        -0.9998666666666667
        1.0
        0.25
        0.25

    Return `BreakPointFunction` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_bpf', '_dc_bias', '_x_values', '_y_range')

    ### INITIALIZER ###

    def __init__(self, bpf):
        from experimental.tools import breakpointtools
        if isinstance(bpf, type(self)):
            assert isinstance(bpf, type(self))
            new_bpf = bpf._bpf.copy()
        elif isinstance(bpf, dict):
            new_bpf = bpf.copy()
            for x, ys in new_bpf.iteritems():
                assert isinstance(x, numbers.Real)
                if isinstance(ys, (list, tuple)):
                    assert len(ys) in (1, 2)
                    assert all(isinstance(y, numbers.Real) for y in ys)
                    new_bpf[x] = tuple(ys)
                elif isinstance(ys, numbers.Real):
                    new_bpf[x] = (ys,)

        self._bpf = new_bpf
        self._update_caches()

    ### SPECIAL METHODS ###

    def __add__(self, other):
        '''Add `other` to all y-values in self:

        ::

            >>> bpf = breakpointtools.BreakPointFunction(
            ...     {0.: 0., 0.75: (-1., 1.), 1.: 0.25})
            >>> bpf + 0.3
            BreakPointFunction({
                0.0: (0.3,),
                0.75: (-0.7, 1.3),
                1.0: (0.55,)
            })

        `other` may also be a BreakPointFunction instance:

        ::

            >>> bpf2 = breakpointtools.BreakPointFunction({0.: 1., 1.: 0.})
            >>> bpf + bpf2
            BreakPointFunction({
                0.0: (1.0,),
                0.75: (-0.75, 1.25),
                1.0: (0.25,)
            })

        Emit new `BreakPointFunction`.
        '''
        return self._operate(other, operator.add)

    def __div__(self, other):
        '''Divide y-values in self by `other`:

        ::

            >>> bpf = breakpointtools.BreakPointFunction(
            ...     {0.: 0., 0.75: (-1., 1.), 1.: 0.25})
            >>> bpf / 2.
            BreakPointFunction({
                0.0: (0.0,),
                0.75: (-0.5, 0.5),
                1.0: (0.125,)
            })

        `other` may also be a `BreakPointFunction` instance.

        Emit new `BreakPointFunction`.
        '''
        return self._operate(other, operator.div)

    def __getitem__(self, item):
        return self.get_y_at_x(item)

    def __mul__(self, other):
        '''Multiply y-values in self by `other`:

        ::

            >>> bpf = breakpointtools.BreakPointFunction(
            ...     {0.: 0., 0.75: (-1., 1.), 1.: 0.25})
            >>> bpf * 2.
            BreakPointFunction({
                0.0: (0.0,),
                0.75: (-2.0, 2.0),
                1.0: (0.5,)
            })

        `other` may also be a `BreakPointFunction` instance.

        Emit new `BreakPointFunction`.
        '''
        return self._operate(other, operator.mul)

    def __sub__(self, other):
        '''Subtract `other` from all y-values in self:

        ::

            >>> bpf = breakpointtools.BreakPointFunction(
            ...     {0.: 0., 0.75: (-1., 1.), 1.: 0.25})
            >>> bpf - 0.3
            BreakPointFunction({
                0.0: (-0.3,),
                0.75: (-1.3, 0.7),
                1.0: (-0.04999999999999999,)
            })

        `other` may also be a BreakPointFunction instance:

        ::

            >>> bpf2 = breakpointtools.BreakPointFunction({0.: 1., 1.: 0.})
            >>> bpf - bpf2
            BreakPointFunction({
                0.0: (-1.0,),
                0.75: (-1.25, 0.75),
                1.0: (0.25,)
            })

        Emit new `BreakPointFunction`.
        '''
        return self._operate(other, operator.sub)

    def __repr__(self):
        result = ['{}({{'.format(self._class_name)]
        if 1 < len(self.x_values):
            for x in self.x_values[:-1]:
                result.append('\t{!r}: {!r},'.format(x, self._bpf[x]))
        result.append('\t{!r}: {!r}'.format(self.x_values[-1], self._bpf[self.x_values[-1]]))
        result.append('})')
        return '\n'.join(result)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def dc_bias(self):
        return self._dc_bias

    @property
    def bpf(self):
        return self._bpf.copy()

    @property
    def gnuplot_format(self):
        raise NotImplemented

    @property
    def x_range(self):
        return self._sorted_xs[0], self._sorted_xs[-1]

    @property
    def x_values(self):
        return tuple(sorted(self._bpf))

    @property
    def y_range(self):
        return self._y_range

    ### PRIVATE METHODS ###

    def _operate(self, other, operator):
        assert isinstance(other, (type(self), numbers.Real))
        if isinstance(other, type(self)):
            x_values = sorted(self.x_values + other.x_values)
        else:
            x_values = self.x_values
        bpf = {}
        for x in x_values:
            if x in self._bpf:
                one_ys = self._bpf[x]
            else:
                one_ys = [self.get_y_at_x(x)]
            if isinstance(other, type(self)):
                if x in other._bpf:
                    two_ys = other._bpf[x]
                else:
                    two_ys = [other.get_y_at_x(x)]
            else:
                two_ys = [other]
            new_ys = []
            if len(one_ys) == len(two_ys):
                if len(one_ys) == 2:
                    new_ys.append(operator(one_ys[0], two_ys[0]))
                    new_ys.append(operator(one_ys[1], two_ys[1]))
                else:
                    new_ys.append(operator(one_ys[0], two_ys[0]))
            elif len(two_ys) < len(one_ys):
                new_ys.append(operator(one_ys[0], two_ys[0]))
                new_ys.append(operator(one_ys[1], two_ys[0]))
            else:
                new_ys.append(operator(two_ys[0], one_ys[0]))
                new_ys.append(operator(two_ys[1], one_ys[0]))
            bpf[x] = new_ys
        return type(self)(bpf)

    def _scale(self, value, old_min, old_max, new_min, new_max):
        raise NotImplemented

    def _update_caches(self): 
        x_values = []
        y_values = []
        for x, ys in self._bpf.iteritems():
            x_values.append(x)
            y_values.extend(ys)
        self._dc_bias = sum(y_values) / len(y_values)
        self._x_values = tuple(sorted(x_values))
        self._y_range = (min(y_values), max(y_values))

    ### PUBLIC METHODS ###

    def clip_x_axis(self, minimum=0, maximum=1):
        raise NotImplemented

    def clip_y_axis(self, minimum=0, maximum=1):
        raise NotImplemented

    def get_y_at_x(self, x):
        '''Get `y`-value at `x`:

        ::

            >>> bpf = breakpointtools.BreakPointFunction(
            ...     {0.: 0., 0.5: (-1., 1.), 1.: 0.5})

        ::

            >>> bpf.get_y_at_x(-1000)
            0.0

        ::

            >>> bpf.get_y_at_x(0.)
            0.0

        ::

            >>> bpf.get_y_at_x(0.25)
            -0.5

        ::

            >>> bpf.get_y_at_x(0.4999)
            -0.9998

        ::

            >>> bpf.get_y_at_x(0.5)
            1.0

        ::

            >>> bpf.get_y_at_x(0.75)
            0.75

        ::

            >>> bpf.get_y_at_x(1.)
            0.5

        ::

            >>> bpf.get_y_at_x(1000)
            0.5

        Return Number.
        '''
        if x <= self.x_values[0]:
            return self._bpf[self.x_values[0]][0]
        elif self.x_values[-1] <= x:
            return self._bpf[self.x_values[-1]][-1]
        elif x in self.x_values:
            return self._bpf[x][-1]
        idx = bisect.bisect(self.x_values, x)
        x0 = self.x_values[idx - 1]
        x1 = self.x_values[idx]
        y0 = self._bpf[x0][-1]
        y1 = self._bpf[x1][0]
        dx = x1 - x0
        dy = y1 - y0
        m = float(dy) / float(dx)
        b = y0 - (m * x0) 
        return (x * m) + b

    def normalize_axes(self):
        raise NotImplemented

    def remove_dc_bias(self):
        return self - self.dc_bias

    def scale_x_axis(self, minimum=0, maximum=1):
        raise NotImplemented

    def scale_y_axis(self, minimum=0, maximum=1):
        raise NotImplemented

    def set_y_at_x(self, x, y):
        assert isinstance(x, numbers.Real)
        if isinstance(y, numbers.Real):
            self._bpf[x] = (y,)
        elif isinstance(y, (list, tuple)):
            assert len(y) in (1, 2) and all(isinstance(j, numbers.Real) for j in y)
            self._bpf[x] = tuple(y)
        elif isinstance(y, type(None)):
            if x in self._bpf:
                del(self._bpf[x])
        else:
            raise ValueError
 
    def tessalate_by_ratio(self, ratio, invert_on_negative=False, reverse_on_negative=False):
        ratio = mathtools.Ratio(ratio)

