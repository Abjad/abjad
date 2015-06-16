# -*- encoding: utf-8 -*-
import bisect
import numbers
import operator
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadObject


class BreakPointFunction(AbjadObject):
    r'''A break-point function:

    ::

        >>> bpf = interpolationtools.BreakPointFunction({
        ...     0.:   0.,
        ...     0.75: (-1, 1.),
        ...     1.:   0.25,
        ...     })

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

    Returns break-point function instance.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bpf',
        '_dc_bias',
        '_x_values',
        '_y_range',
        )

    ### INITIALIZER ###

    def __init__(self, bpf):
        if isinstance(bpf, type(self)):
            assert isinstance(bpf, type(self))
            new_bpf = bpf._bpf.copy()
        elif isinstance(bpf, dict):
            new_bpf = bpf.copy()
            for x, ys in new_bpf.items():
                assert isinstance(x, numbers.Real)
                if isinstance(ys, (list, tuple)):
                    assert len(ys) in (1, 2)
                    assert all(isinstance(y, numbers.Real) for y in ys)
                    if len(ys) == 2 and ys[0] == ys[1]:
                        new_bpf[x] = (ys[0],)
                    else:
                        new_bpf[x] = tuple(ys)
                elif isinstance(ys, numbers.Real):
                    new_bpf[x] = (ys,)
        assert 1 < len(new_bpf)
        self._bpf = new_bpf
        self._update_caches()

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        r'''Add `expr` to all y-values in self:

        ::

            >>> bpf = interpolationtools.BreakPointFunction(
            ...     {0.: 0., 0.75: (-1., 1.), 1.: 0.25})
            >>> bpf + 0.3
            BreakPointFunction({
                0.0: (0.3,),
                0.75: (-0.7, 1.3),
                1.0: (0.55,)
            })

        `expr` may also be a BreakPointFunction instance:

        ::

            >>> bpf2 = interpolationtools.BreakPointFunction({0.: 1., 1.: 0.})
            >>> bpf + bpf2
            BreakPointFunction({
                0.0: (1.0,),
                0.75: (-0.75, 1.25),
                1.0: (0.25,)
            })

        Emit new `BreakPointFunction`.
        '''
        return self._operate(expr, operator.add)

    def __div__(self, expr):
        r'''Divide y-values in self by `expr`:

        ::

            >>> bpf = interpolationtools.BreakPointFunction(
            ...     {0.: 0., 0.75: (-1., 1.), 1.: 0.25})
            >>> bpf / 2.
            BreakPointFunction({
                0.0: (0.0,),
                0.75: (-0.5, 0.5),
                1.0: (0.125,)
            })

        `expr` may also be a `BreakPointFunction` instance.

        Emit new `BreakPointFunction`.
        '''
        return self._operate(expr, operator.truediv)

    __truediv__ = __div__

    def __getitem__(self, item):
        r'''Aliases BreakPointFunction.get_y_at_x().
        '''
        return self.get_y_at_x(item)

    def __mul__(self, expr):
        r'''Multiply y-values in self by `expr`:

        ::

            >>> bpf = interpolationtools.BreakPointFunction(
            ...     {0.: 0., 0.75: (-1., 1.), 1.: 0.25})
            >>> bpf * 2.
            BreakPointFunction({
                0.0: (0.0,),
                0.75: (-2.0, 2.0),
                1.0: (0.5,)
            })

        `expr` may also be a `BreakPointFunction` instance.

        Emit new `BreakPointFunction`.
        '''
        return self._operate(expr, operator.mul)

    def __repr__(self):
        result = ['{}({{'.format(type(self).__name__)]
        if 1 < len(self.x_values):
            for x in self.x_values[:-1]:
                result.append('\t{!r}: {!r},'.format(x, self._bpf[x]))
        result.append('\t{!r}: {!r}'.format(
            self.x_values[-1], self._bpf[self.x_values[-1]]))
        result.append('})')
        return '\n'.join(result)

    def __sub__(self, expr):
        r'''Subtract `expr` from all y-values in self:

        ::

            >>> bpf = interpolationtools.BreakPointFunction(
            ...     {0.: 0., 0.75: (-1., 1.), 1.: 0.25})
            >>> bpf - 0.3
            BreakPointFunction({
                0.0: (-0.3,),
                0.75: (-1.3, 0.7),
                1.0: (-0.04999999999999999,)
            })

        `expr` may also be a BreakPointFunction instance:

        ::

            >>> bpf2 = interpolationtools.BreakPointFunction(
            ...     {0.: 1., 1.: 0.})
            >>> bpf - bpf2
            BreakPointFunction({
                0.0: (-1.0,),
                0.75: (-1.25, 0.75),
                1.0: (0.25,)
            })

        Emit new `BreakPointFunction`.
        '''
        return self._operate(expr, operator.sub)

    ### PUBLIC PROPERTIES ###

    @property
    def bpf(self):
        r'''A copy of the BreakPointFunction's internal data-structure:

        ::

            >>> interpolationtools.BreakPointFunction(
            ...     {0.: 0.25, 0.5: 1.3, 1.: 0.9}).bpf
            {0.0: (0.25,), 0.5: (1.3,), 1.0: (0.9,)}

        Returns dict.
        '''
        return self._bpf.copy()

    @property
    def dc_bias(self):
        r'''The mean y-value of a BreakPointFunction:

        ::

            >>> interpolationtools.BreakPointFunction(
            ...     {0.: 0., 0.25: 0., 0.5: (0.75, 0.25), 1.: 1.}
            ...     ).dc_bias
            0.4

        Returns number.
        '''
        return self._dc_bias

    @property
    def gnuplot_format(self):
        result = [
            "set border lw 1.5 lc rgb '#606060'",
            "set output {filename!r}",
            "set style line 1 lc rgb '#000000' lt 1 lw 2 pt 7 pi -1 ps 1.5",
            "set terminal {image_format} size {width},{height} enhanced",
            "set tics scale 0.75",
            "unset key",
            "plot '-' using 1:2 with linespoints ls 1",
        ]
        for x, ys in sorted(self._bpf.items()):
            if len(ys) == 2:
                result.append('\t{} {}'.format(float(x), float(ys[0])))
                result.append('')
            result.append('\t{} {}'.format(float(x), float(ys[-1])))
        return '\n'.join(result)

    @property
    def x_center(self):
        r'''The arithmetic mean of a BreakPointFunction's x-range:

        ::

            >>> interpolationtools.BreakPointFunction(
            ...     {0.: 0.25, 0.5: 1.3, 1.: 0.9}).x_center
            0.5

        Returns number.
        '''
        return (self.x_range[1] + self.x_range[0]) / 2

    @property
    def x_range(self):
        r'''The minimum and maximum x-values of a BreakPointFunction:

        ::

            >>> interpolationtools.BreakPointFunction(
            ...     {0.: 0.25, 0.5: 1.3, 1.: 0.9}).x_range
            (0.0, 1.0)

        Returns pair.
        '''
        return self.x_values[0], self.x_values[-1]

    @property
    def x_values(self):
        r'''The sorted x-values of a BreakPointFunction:

        ::

            >>> interpolationtools.BreakPointFunction(
            ...     {0.: 0.25, 0.5: 1.3, 1.: 0.9}).x_values
            (0.0, 0.5, 1.0)

        Returns tuple.
        '''
        return tuple(sorted(self._bpf))

    @property
    def y_center(self):
        r'''The arithmetic mean of a BreakPointFunction's y-range:

        ::

            >>> interpolationtools.BreakPointFunction(
            ...     {0.: 0.25, 0.5: 1.3, 1.: 0.9}).y_center
            0.775

        Returns number.
        '''
        return (self.y_range[1] + self.y_range[0]) / 2

    @property
    def y_range(self):
        r'''The minimum and maximum y-values of a BreakPointFunction:

        ::

            >>> interpolationtools.BreakPointFunction(
            ...     {0.: 0.25, 0.5: 1.3, 1.: 0.9}).y_range
            (0.25, 1.3)

        Returns pair.
        '''
        return self._y_range

    ### PRIVATE METHODS ###

    def _operate(self, expr, operator):
        assert isinstance(expr, (type(self), numbers.Real))
        if isinstance(expr, type(self)):
            x_values = sorted(self.x_values + expr.x_values)
        else:
            x_values = self.x_values
        bpf = {}
        for x in x_values:
            if x in self._bpf:
                one_ys = self._bpf[x]
            else:
                one_ys = [self.get_y_at_x(x)]
            if isinstance(expr, type(self)):
                if x in expr._bpf:
                    two_ys = expr._bpf[x]
                else:
                    two_ys = [expr.get_y_at_x(x)]
            else:
                two_ys = [expr]
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
        old_range = old_max - old_min
        new_range = new_max - new_min
        return (((value - old_min) / old_range) * new_range) + new_min

    def _update_caches(self):
        x_values = []
        y_values = []
        for x, ys in self._bpf.items():
            x_values.append(x)
            y_values.extend(ys)
        self._dc_bias = sum(y_values) / len(y_values)
        self._x_values = tuple(sorted(x_values))
        self._y_range = (min(y_values), max(y_values))

    ### PUBLIC METHODS ###

    def clip_x_axis(self, minimum=0, maximum=1):
        r'''Clip x-axis between `minimum` and `maximum`:

        ::

            >>> bpf = interpolationtools.BreakPointFunction(
            ...     {0.: 1., 1.: 0.})
            >>> bpf.clip_x_axis(minimum=0.25, maximum=0.75)
            BreakPointFunction({
                0.25: (0.75,),
                0.75: (0.25,)
            })

        Emit new `BreakPointFunction` instance.
        '''
        assert isinstance(minimum, numbers.Real)
        assert isinstance(maximum, numbers.Real)
        assert minimum < maximum
        bpf = {}
        x_values = [minimum]
        x_values.extend([x for x in self.x_values if minimum < x < maximum])
        x_values.append(maximum)
        for x_value in x_values:
            if x_value in self._bpf:
                bpf[x_value] = self._bpf[x_value]
            else:
                bpf[x_value] = (self[x_value],)
        return type(self)(bpf)

    def clip_y_axis(self, minimum=0, maximum=1):
        r'''Clip y-axis between `minimum` and `maximum`:

        ::

            >>> bpf = interpolationtools.BreakPointFunction(
            ...     {0.: 1., 1.: 0.})
            >>> bpf.clip_y_axis(minimum=0.25, maximum=0.75)
            BreakPointFunction({
                0.0: (0.75,),
                1.0: (0.25,)
            })

        Emit new `BreakPointFunction` instance.
        '''
        assert isinstance(minimum, numbers.Real)
        assert isinstance(maximum, numbers.Real)
        assert minimum < maximum
        bpf = {}
        for x, ys in self._bpf.items():
            new_ys = []
            for y in ys:
                if y < minimum:
                    new_ys.append(minimum)
                elif maximum < y:
                    new_ys.append(maximum)
                else:
                    new_ys.append(y)
            if len(new_ys) == 2 and new_ys[0] == new_ys[1]:
                new_ys.pop()
            bpf[x] = tuple(new_ys)
        return type(self)(bpf)

    def concatenate(self, expr):
        r'''Concatenate self with `expr`:

        ::

            >>> one = interpolationtools.BreakPointFunction(
            ...     {0.0: 0.0, 1.0: 1.0})
            >>> two = interpolationtools.BreakPointFunction(
            ...     {0.5: 0.75, 1.5: 0.25})

        ::

            >>> one.concatenate(two)
            BreakPointFunction({
                0.0: (0.0,),
                1.0: (1.0, 0.75),
                2.0: (0.25,)
            })

        Emit new `BreakPointFunction` instance.
        '''
        assert isinstance(expr, type(self))
        last_x_of_first_bpf = self.x_values[-1]
        first_x_of_second_bpf = expr.x_values[0]
        x_shift = first_x_of_second_bpf - last_x_of_first_bpf
        stop_y = self._bpf[last_x_of_first_bpf][0]
        start_y = expr._bpf[first_x_of_second_bpf][-1]
        hinge_ys = (stop_y, start_y)
        new_bpf_dict = self.bpf
        new_bpf_dict[last_x_of_first_bpf] = hinge_ys
        for x in expr.x_values[1:]:
            new_bpf_dict[x - x_shift] = expr._bpf[x]
        return type(self)(new_bpf_dict)

    def get_y_at_x(self, x):
        r'''Get `y`-value at `x`:

        ::

            >>> bpf = interpolationtools.BreakPointFunction(
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

        Returns Number.
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

    def invert(self, y_center=None):
        r'''Invert self:

        ::

            >>> interpolationtools.BreakPointFunction(
            ...     {0.: 0., 1.: 1.}).invert()
            BreakPointFunction({
                0.0: (1.0,),
                1.0: (0.0,)
            })

        If `y_center` is not None, use `y_center` as the axis of inversion:

        ::

            >>> interpolationtools.BreakPointFunction(
            ...     {0.: 0., 1.: 1.}).invert(0)
            BreakPointFunction({
                0.0: (0.0,),
                1.0: (-1.0,)
            })

        ::

            >>> interpolationtools.BreakPointFunction(
            ...     {0.: 0., 1.: 1.}).invert(0.25)
            BreakPointFunction({
                0.0: (0.5,),
                1.0: (-0.5,)
            })

        Emit new `BreakPointFunction` instance.
        '''
        if y_center is None:
            y_center = self.y_center
        else:
            assert isinstance(y_center, numbers.Real)
        bpf = {}
        for x, ys in self._bpf.items():
            new_ys = [((y_center - y) + y_center) for y in ys]
            bpf[x] = tuple(new_ys)
        return type(self)(bpf)

    def normalize_axes(self):
        r'''Scale both x and y axes between 0 and 1:

        ::

            >>> interpolationtools.BreakPointFunction(
            ...     {0.25: 0.25, 0.75: 0.75}).normalize_axes()
            BreakPointFunction({
                0.0: (0.0,),
                1.0: (1.0,)
            })

        Emit new `BreakPointFunction` instance.
        '''
        return self.scale_x_axis().scale_y_axis()

    def reflect(self, x_center=None):
        r'''Reflect x values of a `BreakPointFunction`:

        ::

            >>> interpolationtools.BreakPointFunction(
            ...     {0.25: 0., 0.5: (-1., 2.), 1: 1.}).reflect()
            BreakPointFunction({
                0.25: (1.0,),
                0.75: (2.0, -1.0),
                1.0: (0.0,)
            })

        If `x_center` is not None, reflection will take `x_center`
        as the axis of reflection:

        ::

            >>> interpolationtools.BreakPointFunction(
            ...     {0.25: 0., 0.5: (-1., 2.), 1: 1.}).reflect(x_center=0.25)
            BreakPointFunction({
                -0.5: (1.0,),
                0.0: (2.0, -1.0),
                0.25: (0.0,)
            })

        Emit new `BreakPointFunction` instance.
        '''
        bpf = {}
        if x_center is None:
            x_center = self.x_center
        else:
            assert isinstance(x_center, numbers.Real)
        for x, ys in self._bpf.items():
            new_x = (x_center - x) + x_center
            bpf[new_x] = tuple(reversed(ys))
        return type(self)(bpf)

    def remove_dc_bias(self):
        r'''Remove dc-bias from a `BreakPointFunction`:

        ::

            >>> interpolationtools.BreakPointFunction(
            ...     {0.: 0., 1.: 1.}).remove_dc_bias()
            BreakPointFunction({
                0.0: (-0.5,),
                1.0: (0.5,)
            })

        Emit new `BreakPointFunction` instance.
        '''
        return self - self.dc_bias

    def scale_x_axis(self, minimum=0, maximum=1):
        r'''Scale x-axis between `minimum` and `maximum`:

        ::

            >>> interpolationtools.BreakPointFunction(
            ...     {0.: 0., 0.5: (-1., 2.), 1.: 1.}
            ...     ).scale_x_axis(-2, 2)
            BreakPointFunction({
                -2.0: (0.0,),
                0.0: (-1.0, 2.0),
                2.0: (1.0,)
            })

        Emit new `BreakPointFunction` instance.
        '''
        assert isinstance(minimum, numbers.Real)
        assert isinstance(maximum, numbers.Real)
        assert minimum < maximum
        bpf = {}
        x_min, x_max = self.x_range
        for x, ys in self._bpf.items():
            bpf[self._scale(x, x_min, x_max, minimum, maximum)] = ys
        return type(self)(bpf)

    def scale_y_axis(self, minimum=0, maximum=1):
        r'''Scale y-axis between `minimum` and `maximum`:

        ::

            >>> interpolationtools.BreakPointFunction(
            ...     {0.: 0., 0.5: (-1., 2.), 1.: 1.}
            ...     ).scale_y_axis(-2, 4)
            BreakPointFunction({
                0.0: (0.0,),
                0.5: (-2.0, 4.0),
                1.0: (2.0,)
            })

        Emit new `BreakPointFunction` instance.
        '''
        assert isinstance(minimum, numbers.Real)
        assert isinstance(maximum, numbers.Real)
        assert minimum < maximum
        bpf = {}
        y_min, y_max = self.y_range
        for x, ys in self._bpf.items():
            bpf[x] = tuple(
                [self._scale(y, y_min, y_max, minimum, maximum) for y in ys])
        return type(self)(bpf)

    def set_y_at_x(self, x, y):
        r'''Set `y`-value at `x`:

        ::

            >>> bpf = interpolationtools.BreakPointFunction(
            ...     {0.0: 0.0, 1.0: 1.0})

        With a number:

        ::

            >>> bpf.set_y_at_x(0.25, 0.75)
            >>> bpf
            BreakPointFunction({
                0.0: (0.0,),
                0.25: (0.75,),
                1.0: (1.0,)
            })

        With a pair:

        ::

            >>> bpf.set_y_at_x(0.6, (-2., 2.))
            >>> bpf
            BreakPointFunction({
                0.0: (0.0,),
                0.25: (0.75,),
                0.6: (-2.0, 2.0),
                1.0: (1.0,)
            })

        Delete all values at `x` when `y` is None:

        ::

            >>> bpf.set_y_at_x(0., None)
            >>> bpf
            BreakPointFunction({
                0.25: (0.75,),
                0.6: (-2.0, 2.0),
                1.0: (1.0,)
            })

        Operates in place and returns None.
        '''
        assert isinstance(x, numbers.Real)
        if isinstance(y, numbers.Real):
            self._bpf[x] = (y,)
        elif isinstance(y, (list, tuple)):
            assert len(y) in (1, 2) and \
                all(isinstance(j, numbers.Real) for j in y)
            if len(y) == 2 and y[0] == y[1]:
                self._bpf[x] = (y[0],)
            else:
                self._bpf[x] = tuple(y)
        elif isinstance(y, type(None)):
            if x in self._bpf:
                del(self._bpf[x])
        else:
            raise ValueError
        self._update_caches()

    def tessalate_by_ratio(self,
        ratio,
        invert_on_negative=False,
        reflect_on_negative=False,
        y_center=None,
        ):
        r'''Concatenate copies of a BreakPointFunction, stretched by
        the weights in `ratio`:

        ::

            >>> bpf = interpolationtools.BreakPointFunction(
            ...     {0.: 0., 0.25: 0.9, 1.: 1.})

        ::

            >>> bpf.tessalate_by_ratio((1, 2, 3))
            BreakPointFunction({
                0.0: (0.0,),
                0.25: (0.9,),
                1.0: (1.0, 0.0),
                1.5: (0.9,),
                3.0: (1.0, 0.0),
                3.75: (0.9,),
                6.0: (1.0,)
            })

        Negative ratio values are still treated as weights.

        If `invert_on_negative` is True, copies corresponding to
        negative ratio values will be inverted:

        ::

            >>> bpf.tessalate_by_ratio((1, -2, 3), invert_on_negative=True)
            BreakPointFunction({
                0.0: (0.0,),
                0.25: (0.9,),
                1.0: (1.0,),
                1.5: (0.09999999999999998,),
                3.0: (0.0,),
                3.75: (0.9,),
                6.0: (1.0,)
            })

        If `y_center` is not None, inversion will take `y_center` as
        the axis of inversion:

        ::

            >>> bpf.tessalate_by_ratio((1, -2, 3),
            ...     invert_on_negative=True, y_center=0)
            BreakPointFunction({
                0.0: (0.0,),
                0.25: (0.9,),
                1.0: (1.0, 0.0),
                1.5: (-0.9,),
                3.0: (-1.0, 0.0),
                3.75: (0.9,),
                6.0: (1.0,)
            })

        If `reflect_on_negative` is True, copies corresponding to
        negative ratio values will be reflected:

        ::

            >>> bpf.tessalate_by_ratio((1, -2, 3), reflect_on_negative=True)
            BreakPointFunction({
                0.0: (0.0,),
                0.25: (0.9,),
                1.0: (1.0,),
                2.5: (0.9,),
                3.0: (0.0,),
                3.75: (0.9,),
                6.0: (1.0,)
            })

        Inversion may be combined reflecting.

        Emit new `BreakPointFunction` instance.
        '''
        ratio = mathtools.Ratio(ratio)
        tessalated_bpf = None
        for i, pair in enumerate(mathtools.cumulative_sums_pairwise(
            [abs(x) for x in ratio.numbers])):
            sign = mathtools.sign(ratio.numbers[i])
            start, stop = pair
            bpf = self.scale_x_axis(start, stop)
            if sign < 0:
                if invert_on_negative:
                    bpf = bpf.invert(y_center)
                if reflect_on_negative:
                    bpf = bpf.reflect()
            if i == 0:
                tessalated_bpf = bpf
            else:
                tessalated_bpf = tessalated_bpf.concatenate(bpf)
        return tessalated_bpf