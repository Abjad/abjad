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
        '''Aliases BreakPointFunction.get_y_at_x().
        '''
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
        '''The mean y-value of a BreakPointFunction:

        ::

            >>> breakpointtools.BreakPointFunction(
            ...     {0.: 0., 0.25: 0., 0.5: (0.75, 0.25), 1.: 1.}
            ...     ).dc_bias
            0.4

        Return number.
        '''
        return self._dc_bias

    @property
    def bpf(self):
        '''A copy of the BreakPointFunction's internal data-structure:

        ::

            >>> breakpointtools.BreakPointFunction({0.: 0.25, 0.5: 1.3, 1.: 0.9}).bpf
            {0.0: (0.25,), 0.5: (1.3,), 1.0: (0.9,)}

        Return dict.
        '''
        return self._bpf.copy()

    @property
    def gnuplot_format(self):
        raise NotImplemented

    @property
    def x_center(self):
        '''The arithmetic mean of a BreakPointFunction's x-range:

        ::

            >>> breakpointtools.BreakPointFunction({0.: 0.25, 0.5: 1.3, 1.: 0.9}).x_center
            0.5

        Return number.
        '''
        return (self.x_range[1] + self.x_range[0]) / 2

    @property
    def x_range(self):
        '''The minimum and maximum x-values of a BreakPointFunction:

        ::

            >>> breakpointtools.BreakPointFunction({0.: 0.25, 0.5: 1.3, 1.: 0.9}).x_range
            (0.0, 1.0)

        Return pair.
        '''
        return self.x_values[0], self.x_values[-1]

    @property
    def x_values(self):
        '''The sorted x-values of a BreakPointFunction:

        ::

            >>> breakpointtools.BreakPointFunction({0.: 0.25, 0.5: 1.3, 1.: 0.9}).x_values
            (0.0, 0.5, 1.0)

        Return tuple.
        '''
        return tuple(sorted(self._bpf))

    @property
    def y_center(self):
        '''The arithmetic mean of a BreakPointFunction's y-range:

        ::

            >>> breakpointtools.BreakPointFunction({0.: 0.25, 0.5: 1.3, 1.: 0.9}).y_center
            0.775

        Return number.
        '''
        return (self.y_range[1] + self.y_range[0]) / 2

    @property
    def y_range(self):
        '''The minimum and maximum y-values of a BreakPointFunction:

        ::

            >>> breakpointtools.BreakPointFunction({0.: 0.25, 0.5: 1.3, 1.: 0.9}).y_range
            (0.25, 1.3)

        Return pair.
        '''
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
        old_range = old_max - old_min
        new_range = new_max - new_min
        return (((value - old_min) / old_range) * new_range) + new_min

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
        '''Clip x-axis between `minimum` and `maximum`:

        ::

            >>> bpf = breakpointtools.BreakPointFunction({0.: 1., 1.: 0.})
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
        '''Clip y-axis between `minimum` and `maximum`:

        ::

            >>> bpf = breakpointtools.BreakPointFunction({0.: 1., 1.: 0.})
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
        for x, ys in self._bpf.iteritems():
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

    def concatenate(self, other):
        '''Concatenate self with `other`:

        ::

            >>> one = breakpointtools.BreakPointFunction({0.0: 0.0, 1.0: 1.0})
            >>> two = breakpointtools.BreakPointFunction({0.5: 0.75, 1.5: 0.25})

        ::

            >>> one.concatenate(two)
            BreakPointFunction({
                0.0: (0.0,),
                1.0: (1.0, 0.75),
                2.0: (0.25,)
            })

        Emit new `BreakPointFunction` instance.
        '''
        assert isinstance(other, type(self))
        last_x_of_first_bpf = self.x_values[-1]
        first_x_of_second_bpf = other.x_values[0]
        x_shift = first_x_of_second_bpf - last_x_of_first_bpf
        stop_y = self._bpf[last_x_of_first_bpf][0]
        start_y = other._bpf[first_x_of_second_bpf][-1]
        hinge_ys = (stop_y, start_y) 
        new_bpf_dict = self.bpf
        new_bpf_dict[last_x_of_first_bpf] = hinge_ys
        for x in other.x_values[1:]:
            new_bpf_dict[x - x_shift] = other._bpf[x]
        return type(self)(new_bpf_dict) 

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

    def invert(self, y_center=None):
        '''Invert self:

        ::

            >>> breakpointtools.BreakPointFunction({0.: 0., 1.: 1.}).invert()
            BreakPointFunction({
                0.0: (1.0,),
                1.0: (0.0,)
            })

        If `y_center` is not None, use `y_center` as the axis of inversion:

        ::

            >>> breakpointtools.BreakPointFunction({0.: 0., 1.: 1.}).invert(0)
            BreakPointFunction({
                0.0: (0.0,),
                1.0: (-1.0,)
            })

        ::

            >>> breakpointtools.BreakPointFunction({0.: 0., 1.: 1.}).invert(0.25)
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
        for x, ys in self._bpf.iteritems():
            new_ys = [((y_center - y) + y_center) for y in ys]
            bpf[x] = tuple(new_ys)
        return type(self)(bpf)

    def normalize_axes(self):
        '''Scale both x and y axes between 0 and 1:

        ::

            >>> breakpointtools.BreakPointFunction({0.25: 0.25, 0.75: 0.75}).normalize_axes()
            BreakPointFunction({
                0.0: (0.0,),
                1.0: (1.0,)
            })

        Emit new `BreakPointFunction` instance.
        '''
        return self.scale_x_axis().scale_y_axis()

    def remove_dc_bias(self):
        '''Remove dc-bias from a `BreakPointFunction`:

        ::

            >>> breakpointtools.BreakPointFunction({0.: 0., 1.: 1.}).remove_dc_bias()
            BreakPointFunction({
                0.0: (-0.5,),
                1.0: (0.5,)
            })

        Emit new `BreakPointFunction` instance.
        '''
        return self - self.dc_bias

    def reflect(self, x_center=None):
        '''Reflect x values of a `BreakPointFunction`:

        ::

            >>> breakpointtools.BreakPointFunction({0.25: 0., 0.5: (-1., 2.), 1: 1.}).reflect()
            BreakPointFunction({
                0.25: (1.0,),
                0.75: (2.0, -1.0),
                1.0: (0.0,)
            })

        If `x_center` is not None, reflection will take `x_center` as the axis of reflection:

        ::

            >>> breakpointtools.BreakPointFunction({0.25: 0., 0.5: (-1., 2.), 1: 1.}).reflect(x_center=0.25)
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
        for x, ys in self._bpf.iteritems():
            new_x = (x_center - x) + x_center
            bpf[new_x] = tuple(reversed(ys))
        return type(self)(bpf)

    def scale_x_axis(self, minimum=0, maximum=1):
        '''Scale x-axis between `minimum` and `maximum`:

        ::

            >>> breakpointtools.BreakPointFunction(
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
        for x, ys in self._bpf.iteritems():
            bpf[self._scale(x, x_min, x_max, minimum, maximum)] = ys
        return type(self)(bpf)

    def scale_y_axis(self, minimum=0, maximum=1):
        '''Scale y-axis between `minimum` and `maximum`:

        ::

            >>> breakpointtools.BreakPointFunction(
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
        for x, ys in self._bpf.iteritems():
            bpf[x] = tuple([self._scale(y, y_min, y_max, minimum, maximum) for y in ys])
        return type(self)(bpf)

    def set_y_at_x(self, x, y):
        '''Set `y`-value at `x`:

        ::

            >>> bpf = breakpointtools.BreakPointFunction({0.0: 0.0, 1.0: 1.0})

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

        Operate in place and return None.
        '''
        assert isinstance(x, numbers.Real)
        if isinstance(y, numbers.Real):
            self._bpf[x] = (y,)
        elif isinstance(y, (list, tuple)):
            assert len(y) in (1, 2) and all(isinstance(j, numbers.Real) for j in y)
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
 
    def tessalate_by_ratio(self, ratio, invert_on_negative=False, reflect_on_negative=False,
        y_center=None):
        '''Concatenate copies of a BreakPointFunction, stretched by the weights in `ratio`:

        ::

            >>> bpf = breakpointtools.BreakPointFunction({0.: 0., 0.25: 0.9, 1.: 1.})

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

        If `invert_on_negative` is True, copies corresponding to negative ratio values
        will be inverted:

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

        If `y_center` is not None, inversion will take `y_center` as the axis of inversion:

        ::

            >>> bpf.tessalate_by_ratio((1, -2, 3), invert_on_negative=True, y_center=0)
            BreakPointFunction({
                0.0: (0.0,),
                0.25: (0.9,),
                1.0: (1.0, 0.0),
                1.5: (-0.9,),
                3.0: (-1.0, 0.0),
                3.75: (0.9,),
                6.0: (1.0,)
            })

        If `reflect_on_negative` is True, copies corresponding to negative ratio values
        will be reflectd:

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
        for i, pair in enumerate(mathtools.cumulative_sums_zero_pairwise(
            [abs(x) for x in ratio])):
            sign = mathtools.sign(ratio[i])
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
            
