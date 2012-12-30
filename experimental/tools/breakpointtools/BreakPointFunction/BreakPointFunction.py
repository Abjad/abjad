import numbers
from abjad.tools.abctools import AbjadObject


class BreakPointFunction(AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_bpf', '_sorted_xs',)

    ### INITIALIZER ###

    def __init__(self, *args):
        if len(args) == 1:
            assert isinstance(args[0], type(self))
            points = args[0].points
        else:
            assert sequencetools.all_are_pairs_of_types(
                args, numbers.Real, numbers.Real)
            points = args

        bpf = {}
        for x, y in points:
            if x not in bpf:
                bpf[x] = [y, None] # left, right bounds
            else:
                bpf[x][1] = y

        sorted_xs = sorted(bpf[:])
             
        self._bpf = bpf
        self._sorted_xs = sorted_xs           

    ### READ-ONLY PRIVATE ATTRIBUTES ###

    @property
    def _positional_argument_names(self):
        return ('points',)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def maximum_x(self):
        return self._sorted_xs[0]

    @property
    def maximum_y(self):
        raise NotImplemented

    @property
    def maximum_y(self):
        raise NotImplemented

    @property
    def minimum_x(self):
        return self._sorted_xs[-1]

    @property
    def points(self):
        raise NotImplemented

    ### PUBLIC METHODS ###

    def clip_x_axis(self, minimum=0, maximum=1):
        raise NotImplemented

    def clip_y_axis(self, minimum=0, maximum=1):
        raise NotImplemented

    def get_y_at_x(self, x, right=True):
        raise NotImplemented

    def normalize_axes(self):
        raise NotImplemented

    def scale_x_axis(self, minimum=0, maximum=1):
        raise NotImplemented

    def scale_y_axis(self, minimum=0, maximum=1):
        raise NotImplemented

    def set_y_at_x(self, x, right=True):
        raise NotImplemented

    
