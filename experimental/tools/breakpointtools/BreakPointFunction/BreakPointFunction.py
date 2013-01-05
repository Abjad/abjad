import numbers
import operator
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadObject


class BreakPointFunction(AbjadObject):
    '''A break-point function:

    ::

        >>> from experimental.tools import breakpointtools

    ::

        >>> bpf = breakpointtools.BreakPointFunction({0.: 0., 0.5: 1., 1.: 0.25})

    Return `BreakPointFunction` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_bpf', '_x_values', '_y_range')

    ### INITIALIZER ###

    def __init__(self, *args):
        from experimental.tools import breakpointtools
        if len(args) == 1:
            if isinstance(args[0], type(self)):
                assert isinstance(args[0], type(self))
                new_bpf = args[0]._bpf.copy()
            elif isinstance(args[0], dict):
                for x, ys in args[0].iteritems():
                    assert isinstance(x, numbers.Real)
                    assert isinstance(ys, (numbers.Real, list, tuple))
                    if isinstance(ys, (list, tuple)):
                        assert len(ys) in (1, 2)
                        assert all(isinstance(y, numbers.Real) for y in ys)
                new_bpf = args[0].copy()
                for x, ys in new_bpf.iteritems():
                    if isinstance(ys, numbers.Real):
                        new_bpf[x] = (ys,)
                    elif isinstance(ys, list):
                        new_bpf[x] = tuple(ys)
        else:
            points = [breakpointtools.BreakPoint(*arg) for arg in args]
            new_bpf = {}
            for point in points:
                if point.x not in new_bpf:
                    new_bpf[point.x] = (point.y,)
                else:
                    current = new_bpf[point.x]
                    new_bpf[point.x] = (new_bpf[point.x][0], point.y)

        self._bpf = new_bpf
        self._x_values = sorted(new_bpf)
        self._update_y_range()

    ### SPECIAL METHODS ###

    def __add__(self, other):
        return self._operate(other, operators.add)

    def __div__(self, other):
        return self._operate(other, operators.div)

    def __mul__(self, other):
        return self._operate(other, operators.mul)

    def __sub__(self, other):
        return self._operate(other, operators.sub)

    def __repr__(self):
        result = ['{}({{'.format(self._class_name)]
        if 1 < len(self.x_values):
            for x in self.x_values:
                result.append('\t{!r}: {!r},'.format(x, self._bpf[x]))
        result.append('\t{!r}: {!r}'.format(self.x_values[-1], self._bpf[self.x_values[-1]]))
        result.append('})')
        return '\n'.join(result)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

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
            all_xs = sorted(self.x_values + other.x_values)
        else:
            all_xs = self.x_values
        new_bpf = {}
        for x in xs:
            if x in self._bpf:
                one_ys = [breakpoint.y for breakpoint in self._bpf[x]]
            else:
                one_ys = [self.get_y_at_x(x)]
            if isinstance(other, type(self)):
                if x in other._bpf:
                    two_ys = [breakpoint.y for breakpoint in other._bpf[x]]
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
                    new_ys.append(None)
                    new_ys.append(operator(one_ys[0], two_ys[0]))
            elif len(two_ys) < len(one_ys):
                new_ys.append(operator(one_ys[0], two_ys[0]))
                new_ys.append(operator(one_ys[1], two_ys[0]))
            else:
                new_ys.append(operator(two_ys[0], one_ys[0]))
                new_ys.append(operator(two_ys[1], one_ys[0]))
            new_bpf[x] = new_ys
        bpf = type(self)()

    def _scale(self, value, old_min, old_max, new_min, new_max):
        raise NotImplemented

    def _update_y_range(self):
        y_values = set([])
        for ys in self._bpf.itervalues():
            y_values.update(ys)
        self._y_range = (min(y_values), max(y_values))

    ### PUBLIC METHODS ###

    def clip_x_axis(self, minimum=0, maximum=1):
        raise NotImplemented

    def clip_y_axis(self, minimum=0, maximum=1):
        raise NotImplemented

    def get_y_at_x(self, x):
        raise NotImplemented

    def normalize_axes(self):
        raise NotImplemented

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
 
    def tesselate_by_ratio(self, ratio, invert_on_negative=False, reverse_on_negative=False):
        ratio = mathtools.Ratio(ratio)

