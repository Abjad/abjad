from abjad.tools.datastructuretools import ImmutableDictionary
from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.TimeIntervalAggregateMixin import TimeIntervalAggregateMixin


class TimeIntervalTreeDictionary(TimeIntervalAggregateMixin, ImmutableDictionary):

    __slots__ = ('_composite_tree', '_start', '_stop')

    def __init__(self, *args):
        assert 0 < len(args)
        if len(args) == 1 and isinstance(args[0], type(self)):
            dict.update(self, args)
            object.__setattr__(self, '_composite_tree', args[0].composite_tree)
            object.__setattr__(self, '_start', args[0].start)
            object.__setattr__(self, '_stop', args[0].stop)
        else:
            if isinstance(args[0], dict):
                args = args[0].items( )
            assert all_are_pairs(args)
            key, tree = args[0]
            assert isinstance(tree, IntervalTree)
            dict.__setitem__(self, key, tree)
            object.__setattr__(self, '_start', tree.start)
            object.__setattr__(self, '_stop', tree.stop)
            for key, tree in args[1:]:
                assert isinstance(tree, IntervalTree)
                if not tree:
                    continue
                if tree.start < self.start:
                    object.__setattr__(self, '_start', tree.start)
                if self.stop < tree.stop:
                    object.__setattr__(self, '_stop', tree.stop)
                dict.__setitem__(self, performer, tree)
            object.__setattr__(self, '_composite_tree', TimeIntervalTree(self.values()))

    ### PUBLIC ATTRIBUTES ###

    @property
    def composite_tree(self):
        return self._composite_tree

    ### PUBLIC METHODS ###

    def quantize_to_rational(self, rational):
        pass

    def scale_by_rational(self, rational):
        pass

    def scale_to_rational(self, rational):
        pass

    def shift_by_rational(self, rational):
        pass

    def shift_to_rational(self, rational):
        pass

    def split_at_rationals(self, *rationals):
        pass
