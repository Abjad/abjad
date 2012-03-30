from abjad.tools.datastructuretools import ImmutableDictionary
from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.TimeIntervalAggregateMixin import TimeIntervalAggregateMixin


class TimeIntervalTreeDictionary(TimeIntervalAggregateMixin, ImmutableDictionary):

    __slots__ = ('_composite_tree', '_start', '_stop')

    def __init__(self, *args):
        #assert 0 < len(args)
        if len(args) == 1 and isinstance(args[0], type(self)):
            dict.update(self, args)
            object.__setattr__(self, '_composite_tree', args[0].composite_tree)
            object.__setattr__(self, '_start', args[0].start)
            object.__setattr__(self, '_stop', args[0].stop)
        else:
            if isinstance(args[0], dict):
                args = args[0].items( )

            if args:
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

            else:
                object.__setattr__(self, '_start', None)
                object.__setattr__(self, '_stop', None)
            
            object.__setattr__(self, '_composite_tree', TimeIntervalTree(self.values()))

    ### PUBLIC ATTRIBUTES ###

    @property
    def composite_tree(self):
        return self._composite_tree

    @property
    def earliest_start(self):
        return self.composite_tree.earliest_start

    @property
    def earliest_stop(self):
        return self.composite_tree.earliest_stop

    @property
    def latest_start(self):
        return self.composite_tree.latest_start

    @property
    def latest_stop(self):
        return self.composite_tree.latest_stop

    @property
    def trees(self):
        return self.keys()

    ### PUBLIC METHODS ###

    def find_intervals_intersecting_or_tangent_to_interval(self, *args):
        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_intersecting_or_tangent_to_interval(*args)
            if len(tree):
                result[key] = found
        return type(self)(result)

    def find_intervals_intersecting_or_tangent_to_offset(self, offset):
        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_intersecting_or_tangent_to_offset(offset)
            if len(tree):
                result[key] = found
        return type(self)(result)

    def find_intervals_starting_after_offset(self, offset):
        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_starting_after_offset(offset)
            if len(tree):
                result[key] = found
        return type(self)(result)

    def find_intervals_starting_and_stopping_within_interval(self, *args):
        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_starting_and_stopping_within_interval(*args)
            if len(tree):
                result[key] = found
        return type(self)(result)

    def find_intervals_starting_at_offset(self, offset):
        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_starting_at_offset(offset)
            if len(tree):
                result[key] = found
        return type(self)(result)

    def find_intervals_starting_before_offset(self, offset):
        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_starting_before_offset(offset)
            if len(tree):
                result[key] = found
        return type(self)(result)

    def find_intervals_starting_or_stopping_at_offset(self, offset):
        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_starting_or_stopping_at_offset(offset)
            if len(tree):
                result[key] = found
        return type(self)(result)

    def find_intervals_starting_within_interval(self, *args):
        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_starting_within_interval(*args)
            if len(tree):
                result[key] = found
        return type(self)(result)

    def find_intervals_stopping_after_offset(self, offset):
        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_stopping_after_offset(offset)
            if len(tree):
                result[key] = found
        return type(self)(result)

    def find_intervals_stopping_at_offset(self, offset):
        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_stopping_at_offset(offset)
            if len(tree):
                result[key] = found
        return type(self)(result)

    def find_intervals_stopping_before_offset(self, offset):
        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_stopping_before_offset(offset)
            if len(tree):
                result[key] = found
        return type(self)(result)

    def find_intervals_stopping_within_interval(self, *args):
        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_stopping_within_interval(*args)
            if len(tree):
                result[key] = found
        return type(self)(result)

    def quantize_to_rational(self, rational):
        rational = Duration(rational)
        result = {}
        for key, tree in self.iteritems():
            result[key] = tree.quantize_to_rational(rational)
        return type(self)(result)

    def scale_by_rational(self, rational):
        rational = Duration(rational)
        result = {}
        for key, tree in self.iteritems():
            offset = (tree.start - self.start) * rational
            result[key] = tree.scale_by_rational(rational).shift_to_rational(self.start + offset)
        return type(self)(result)

    def scale_to_rational(self, rational):
        rational = Duration(rational)
        result = {}
        for key, tree in self.iteritems():
            offset = ((tree.start - self.start) * rational * (tree.start / self.stop))
            duration = (tree.duration / self.duration) * rational
            result[key] = tree.scale_to_rational(duration).shift_to_rational(self.start + offset)
        return type(self)(result)

    def shift_by_rational(self, rational):
        rational = Offset(rational)
        result = {}
        for key, tree in self.iteritems():
            result[key] = tree.shift_by_rational(rational)
        return type(self)(result)

    def shift_to_rational(self, rational):
        rational = Offset(rational)
        result = {}
        for key, tree in self.iteritems():
            offset = tree.start - self.start
            result[key] = tree.shift_to_rational(rational + offset)
        return type(self)(result)

    def split_at_rationals(self, *rationals):
        assert 0 < len(rationals)
        rationals = sorted([Offset(x) for x in rationals])
        rationals = [x for x in rationals if self.start < x < self.stop]
        dicts = []
        carried = dict(self)
        for rational in rationals:
            result = {}
            for key, tree in carried.iteritems():
                splits = tree.split_at_rationals(rational)
                if len(splits) == 2:
                    result[key] = splits[0]
                    carried[key] = splits[1]
                elif splits[0].stop <= rational:
                    result[key] = splits[0]
                    del(carried[key])
                elif rational <= splits[0].start:
                    pass
                else:
                    raise Exception('Tree failed to split.')
            if result:
                dicts.append(type(self)(result))
        if carried:
            dicts.append(type(self)(carried))
        return tuple(dicts)
