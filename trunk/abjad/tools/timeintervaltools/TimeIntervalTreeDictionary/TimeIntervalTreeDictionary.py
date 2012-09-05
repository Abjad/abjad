from abjad.tools import abctools
from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools.datastructuretools import ImmutableDictionary
from abjad.tools.timeintervaltools.TimeIntervalAggregateMixin import TimeIntervalAggregateMixin


class TimeIntervalTreeDictionary(TimeIntervalAggregateMixin, ImmutableDictionary):
    '''A dictionary of `TimeIntervalTrees`:

    ::

        >>> from abjad.tools.timeintervaltools import TimeIntervalTreeDictionary

    ::

        >>> from abjad.tools.timeintervaltools import TimeIntervalTree
        >>> from abjad.tools.timeintervaltools import TimeInterval

    ::

        >>> a = TimeIntervalTree([TimeInterval(0, 1, {'name': 'a'})])
        >>> b = TimeIntervalTree([TimeInterval(1, 2, {'name': 'b'})])
        >>> c = TimeIntervalTree([TimeInterval(0, 3, {'name': 'c'})])
        >>> d = TimeIntervalTree([TimeInterval(2, 3, {'name': 'd'})])
        >>> treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})
        >>> treedict
        TimeIntervalTreeDictionary({
            'a': TimeIntervalTree([
                TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
            ]),
            'b': TimeIntervalTree([
                TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
            ]),
            'c': TimeIntervalTree([
                TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
            ]),
            'd': TimeIntervalTree([
                TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
            ]),
        })


    `TimeIntervalTreeDictionary` can be instantiated from one or more other
    `TimeIntervalTreeDictionary` instances, whose trees will be fused if they
    share keys.  It can also be instantiated from a regular dictionary whose
    values are `TimeIntervalTree` instances, or from a list of pairs where the
    second value of each pair is a `TimeIntervalTree` instance.

    `TimeIntervalTreeDictionary` supports the same set of methods and
    properties as `TimeIntervalTree` and `TimeInterval`, including searching
    for intervals, quantizing, scaling, shifting and splitting.


    `TimeIntervalTreeDictionary` is immutable.

    Return `TimeIntervalTreeDictionary` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_composite_tree', '_start', '_stop')

    #### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools import timeintervaltools

        # should be the same
        if len(args) == 1 and isinstance(args[0], type(self)):
            result = args[0]
            dict.update(self, result)
            object.__setattr__(self, '_composite_tree', result.composite_tree)
            object.__setattr__(self, '_start', result.start)
            object.__setattr__(self, '_stop', result.stop)

        # fuse dictionaries keywise
        elif 1 < len(args) and all([isinstance(x, type(self)) for x in args]):
            result = { }
            for arg in args:
                for key, tree in arg.iteritems():
                    if key in result:
                        result[key] = timeintervaltools.TimeIntervalTree([result[key], tree])
                    else:
                        result[key] = tree
            dict.update(self, result)
            object.__setattr__(self, '_composite_tree', timeintervaltools.TimeIntervalTree(self.values()))
            object.__setattr__(self, '_start', self.composite_tree.start)
            object.__setattr__(self, '_stop', self.composite_tree.stop)

        # unpack a regular dict as pairs, or simply accept pairs
        else:
            if isinstance(args[0], dict):
                args = args[0].items()

            if args:
                assert sequencetools.all_are_pairs(args)
                key, tree = args[0]
                assert isinstance(tree, timeintervaltools.TimeIntervalTree)
                dict.__setitem__(self, key, tree)
                for key, tree in args[1:]:
                    assert isinstance(tree, timeintervaltools.TimeIntervalTree)
                    dict.__setitem__(self, key, tree)

            else:
                object.__setattr__(self, '_start', None)
                object.__setattr__(self, '_stop', None)
            
            object.__setattr__(self, '_composite_tree', timeintervaltools.TimeIntervalTree(self.values()))
            object.__setattr__(self, '_start', self.composite_tree.start)
            object.__setattr__(self, '_stop', self.composite_tree.stop)

    ### SPECIAL METHODS ###

    def __repr__(self):
        if not self:
            return '%s({})' % self._class_name
        pieces = ['%s({' % self._class_name]
        for key in sorted(self.keys()):
            tree = self[key]
            if not tree:
                pieces.append('\t%r: %s' % (key, tree))
            else:
                pieces.append('\t%r: %s([' % (key, type(tree).__name__))
                for interval in tree:
                    pieces.append('\t\t%r,' % interval)
                pieces.append('\t]),')
        pieces.append('})')
        return '\n'.join(pieces)

    ### PUBLIC PROPERTIES ###

    @property
    def composite_tree(self):
        '''The `TimeIntervalTree` composed of all the intervals in all trees in
        self:

        ::

            >>> a = TimeIntervalTree([TimeInterval(0, 1, {'name': 'a'})])
            >>> b = TimeIntervalTree([TimeInterval(1, 2, {'name': 'b'})])
            >>> c = TimeIntervalTree([TimeInterval(0, 3, {'name': 'c'})])
            >>> d = TimeIntervalTree([TimeInterval(2, 3, {'name': 'd'})])
            >>> treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})

        ::

            >>> treedict.composite_tree
            TimeIntervalTree([
                TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'})
            ])

        Return `TimeIntervalTree` instance.
        '''
        return self._composite_tree

    @property
    def earliest_start(self):
        '''The earliest start offset of all intervals in all trees in self:

        ::

            >>> a = TimeIntervalTree([TimeInterval(0, 1, {'name': 'a'})])
            >>> b = TimeIntervalTree([TimeInterval(1, 2, {'name': 'b'})])
            >>> c = TimeIntervalTree([TimeInterval(0, 3, {'name': 'c'})])
            >>> d = TimeIntervalTree([TimeInterval(2, 3, {'name': 'd'})])
            >>> treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})

        ::

            >>> treedict.earliest_start
            Offset(0, 1)

        Return `Offset` instance.
        '''
        return self.composite_tree.earliest_start

    @property
    def earliest_stop(self):
        '''The earliest stop offset of all intervals in all trees in self:

        ::

            >>> a = TimeIntervalTree([TimeInterval(0, 1, {'name': 'a'})])
            >>> b = TimeIntervalTree([TimeInterval(1, 2, {'name': 'b'})])
            >>> c = TimeIntervalTree([TimeInterval(0, 3, {'name': 'c'})])
            >>> d = TimeIntervalTree([TimeInterval(2, 3, {'name': 'd'})])
            >>> treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})

        ::

            >>> treedict.earliest_stop
            Offset(1, 1)

        Return `Offset` instance.
        '''
        return self.composite_tree.earliest_stop

    @property
    def intervals(self):
        return tuple(self.composite_tree[:])

    @property
    def latest_start(self):
        '''The latest start offset of all intervals in all trees in self:

        ::

            >>> a = TimeIntervalTree([TimeInterval(0, 1, {'name': 'a'})])
            >>> b = TimeIntervalTree([TimeInterval(1, 2, {'name': 'b'})])
            >>> c = TimeIntervalTree([TimeInterval(0, 3, {'name': 'c'})])
            >>> d = TimeIntervalTree([TimeInterval(2, 3, {'name': 'd'})])
            >>> treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})

        ::

            >>> treedict.latest_start
            Offset(2, 1)

        Return `Offset` instance.
        '''
        return self.composite_tree.latest_start

    @property
    def latest_stop(self):
        '''The latest stop offset of all intervals in all trees in self:

        ::

            >>> a = TimeIntervalTree([TimeInterval(0, 1, {'name': 'a'})])
            >>> b = TimeIntervalTree([TimeInterval(1, 2, {'name': 'b'})])
            >>> c = TimeIntervalTree([TimeInterval(0, 3, {'name': 'c'})])
            >>> d = TimeIntervalTree([TimeInterval(2, 3, {'name': 'd'})])
            >>> treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})

        ::

            >>> treedict.latest_stop
            Offset(3, 1)

        Return `Offset` instance.
        '''
        return self.composite_tree.latest_stop

    ### PRIVATE METHODS ###

    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        if not len(self):
            return ['{}({{}})'.format(self._tools_package_qualified_class_name)]

        pieces = []
        pieces.append('{}({{'.format(self._tools_package_qualified_class_name))

        for key, tree in self.iteritems():
            if isinstance(key, abctools.AbjadObject):
                kpieces = key._get_tools_package_qualified_repr_pieces()
            else:
                kpieces = [repr(key)]
            tpieces = tree._get_tools_package_qualified_repr_pieces()

            if 1 == len(kpieces):
                if 1 == len(tpieces):
                    pieces.append('\t{}: {},'.format(kpieces[0], tpieces[0]))
                else:
                    pieces.append('\t{}: {}'.format(kpieces[0], tpieces[0]))
                    for tpiece in tpieces[1:-1]:
                        pieces.append('\t{}'.format(tpiece))
                    pieces.append('\t{},'.format(tpieces[-1]))

            else:
                for kpiece in kpieces[:-1]:
                    pieces.append('\t{}'.format(kpiece))
                if 1 == len(tpieces):
                    pieces.append('\t{}: {},'.format(kpieces[-1], tpieces[0]))
                else:
                    pieces.append('\t{}: {}'.format(kpieces[-1], tpieces[0]))
                    for tpiece in tpieces[1:-1]:
                        pieces.append('\t{}'.format(tpiece))
                    pieces.append('\t{},'.format(tpieces[-1]))

        pieces.append('\t})')

        return pieces

    ### PUBLIC METHODS ###

    def find_intervals_intersecting_or_tangent_to_interval(self, *args):
        '''Find all intervals in dictionary intersecting or tangent to the interval
        defined in `args`:

        ::

            >>> a = TimeIntervalTree([TimeInterval(0, 1, {'name': 'a'})])
            >>> b = TimeIntervalTree([TimeInterval(1, 2, {'name': 'b'})])
            >>> c = TimeIntervalTree([TimeInterval(0, 3, {'name': 'c'})])
            >>> d = TimeIntervalTree([TimeInterval(2, 3, {'name': 'd'})])
            >>> treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})
            >>> treedict
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        ::

            >>> interval = TimeInterval(0, 1)
            >>> treedict.find_intervals_intersecting_or_tangent_to_interval(interval)
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
            })            

        ::

            >>> interval = TimeInterval(3, 4)
            >>> treedict.find_intervals_intersecting_or_tangent_to_interval(interval)
            TimeIntervalTreeDictionary({
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        Return `TimeIntervalTreeDictionary` instance.
        '''

        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_intersecting_or_tangent_to_interval(*args)
            if len(found):
                result[key] = found
        return type(self)(result)

    def find_intervals_intersecting_or_tangent_to_offset(self, offset):
        '''Find all intervals in dictionary intersecting or tangent to `offset`:

        ::

            >>> a = TimeIntervalTree([TimeInterval(0, 1, {'name': 'a'})])
            >>> b = TimeIntervalTree([TimeInterval(1, 2, {'name': 'b'})])
            >>> c = TimeIntervalTree([TimeInterval(0, 3, {'name': 'c'})])
            >>> d = TimeIntervalTree([TimeInterval(2, 3, {'name': 'd'})])
            >>> treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})
            >>> treedict
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        ::

            >>> offset = 1
            >>> treedict.find_intervals_intersecting_or_tangent_to_offset(offset)
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
            })

        ::

            >>> offset = 3
            >>> treedict.find_intervals_intersecting_or_tangent_to_offset(offset)
            TimeIntervalTreeDictionary({
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        Return `TimeIntervalTreeDictionary` instance.
        '''

        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_intersecting_or_tangent_to_offset(offset)
            if len(found):
                result[key] = found
        return type(self)(result)

    def find_intervals_starting_after_offset(self, offset):
        '''Find all intervals in dictionary starting after `offset`:

        ::

            >>> a = TimeIntervalTree([TimeInterval(0, 1, {'name': 'a'})])
            >>> b = TimeIntervalTree([TimeInterval(1, 2, {'name': 'b'})])
            >>> c = TimeIntervalTree([TimeInterval(0, 3, {'name': 'c'})])
            >>> d = TimeIntervalTree([TimeInterval(2, 3, {'name': 'd'})])
            >>> treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})
            >>> treedict
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        ::

            >>> offset = 0
            >>> treedict.find_intervals_starting_after_offset(offset)
            TimeIntervalTreeDictionary({
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        ::

            >>> offset = 1
            >>> treedict.find_intervals_starting_after_offset(offset)
            TimeIntervalTreeDictionary({
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        Return `TimeIntervalTreeDictionary` instance.
        '''

        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_starting_after_offset(offset)
            if len(found):
                result[key] = found
        return type(self)(result)

    def find_intervals_starting_and_stopping_within_interval(self, *args):
        '''Find all intervals in dictionary starting and stopping within the interval
        defined by `args`:

        ::

            >>> a = TimeIntervalTree([TimeInterval(0, 1, {'name': 'a'})])
            >>> b = TimeIntervalTree([TimeInterval(1, 2, {'name': 'b'})])
            >>> c = TimeIntervalTree([TimeInterval(0, 3, {'name': 'c'})])
            >>> d = TimeIntervalTree([TimeInterval(2, 3, {'name': 'd'})])
            >>> treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})
            >>> treedict
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        ::

            >>> interval = TimeInterval(1, 3)
            >>> treedict.find_intervals_starting_and_stopping_within_interval(interval)
            TimeIntervalTreeDictionary({
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        ::

            >>> interval = TimeInterval(-1, 2)
            >>> treedict.find_intervals_starting_and_stopping_within_interval(interval)
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
            })

        Return `TimeIntervalTreeDictionary` instance.
        '''

        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_starting_and_stopping_within_interval(*args)
            if len(found):
                result[key] = found
        return type(self)(result)

    def find_intervals_starting_at_offset(self, offset):
        '''Find all intervals in dictionary starting at `offset`:

        ::

            >>> a = TimeIntervalTree([TimeInterval(0, 1, {'name': 'a'})])
            >>> b = TimeIntervalTree([TimeInterval(1, 2, {'name': 'b'})])
            >>> c = TimeIntervalTree([TimeInterval(0, 3, {'name': 'c'})])
            >>> d = TimeIntervalTree([TimeInterval(2, 3, {'name': 'd'})])
            >>> treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})
            >>> treedict
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        ::

            >>> offset = 0
            >>> treedict.find_intervals_starting_at_offset(offset)
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
            })

        ::

            >>> offset = 1
            >>> treedict.find_intervals_starting_at_offset(offset)
            TimeIntervalTreeDictionary({
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
            })

        Return `TimeIntervalTreeDictionary` instance.
        '''

        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_starting_at_offset(offset)
            if len(found):
                result[key] = found
        return type(self)(result)

    def find_intervals_starting_before_offset(self, offset):
        '''Find all intervals in dictionary starting before `offset`:

        ::

            >>> a = TimeIntervalTree([TimeInterval(0, 1, {'name': 'a'})])
            >>> b = TimeIntervalTree([TimeInterval(1, 2, {'name': 'b'})])
            >>> c = TimeIntervalTree([TimeInterval(0, 3, {'name': 'c'})])
            >>> d = TimeIntervalTree([TimeInterval(2, 3, {'name': 'd'})])
            >>> treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})
            >>> treedict
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        ::

            >>> offset = 1
            >>> treedict.find_intervals_starting_before_offset(offset)
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
            })

        ::

            >>> offset = 2
            >>> treedict.find_intervals_starting_before_offset(offset)
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
            })

        Return `TimeIntervalTreeDictionary` instance.
        '''

        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_starting_before_offset(offset)
            if len(found):
                result[key] = found
        return type(self)(result)

    def find_intervals_starting_or_stopping_at_offset(self, offset):
        '''Find all intervals in dictionary starting or stopping at `offset`:

        ::

            >>> a = TimeIntervalTree([TimeInterval(0, 1, {'name': 'a'})])
            >>> b = TimeIntervalTree([TimeInterval(1, 2, {'name': 'b'})])
            >>> c = TimeIntervalTree([TimeInterval(0, 3, {'name': 'c'})])
            >>> d = TimeIntervalTree([TimeInterval(2, 3, {'name': 'd'})])
            >>> treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})
            >>> treedict
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        ::

            >>> offset = 2 
            >>> treedict.find_intervals_starting_or_stopping_at_offset(offset)
            TimeIntervalTreeDictionary({
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        ::

            >>> offset = 1
            >>> treedict.find_intervals_starting_or_stopping_at_offset(offset)
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
            })

        Return `TimeIntervalTreeDictionary` instance.
        '''

        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_starting_or_stopping_at_offset(offset)
            if len(found):
                result[key] = found
        return type(self)(result)

    def find_intervals_starting_within_interval(self, *args):
        '''Find all intervals in dictionary starting within the interval defined by
        `args`:

        ::

            >>> a = TimeIntervalTree([TimeInterval(0, 1, {'name': 'a'})])
            >>> b = TimeIntervalTree([TimeInterval(1, 2, {'name': 'b'})])
            >>> c = TimeIntervalTree([TimeInterval(0, 3, {'name': 'c'})])
            >>> d = TimeIntervalTree([TimeInterval(2, 3, {'name': 'd'})])
            >>> treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})
            >>> treedict
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        ::

            >>> interval = TimeInterval((-1, 2), (1, 2))
            >>> treedict.find_intervals_starting_within_interval(interval)
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
            })

        ::

            >>> interval = TimeInterval((1, 2), (5, 2))
            >>> treedict.find_intervals_starting_within_interval(interval)
            TimeIntervalTreeDictionary({
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        Return `TimeIntervalTreeDictionary` instance.
        '''

        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_starting_within_interval(*args)
            if len(found):
                result[key] = found
        return type(self)(result)

    def find_intervals_stopping_after_offset(self, offset):
        '''Find all intervals in dictionary stopping after `offset`:

        ::

            >>> a = TimeIntervalTree([TimeInterval(0, 1, {'name': 'a'})])
            >>> b = TimeIntervalTree([TimeInterval(1, 2, {'name': 'b'})])
            >>> c = TimeIntervalTree([TimeInterval(0, 3, {'name': 'c'})])
            >>> d = TimeIntervalTree([TimeInterval(2, 3, {'name': 'd'})])
            >>> treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})
            >>> treedict
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        ::

            >>> offset = 1
            >>> treedict.find_intervals_stopping_after_offset(offset)
            TimeIntervalTreeDictionary({
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        ::

            >>> offset = 2
            >>> treedict.find_intervals_stopping_after_offset(offset)
            TimeIntervalTreeDictionary({
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        Return `TimeIntervalTreeDictionary` instance.
        '''

        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_stopping_after_offset(offset)
            if len(found):
                result[key] = found
        return type(self)(result)

    def find_intervals_stopping_at_offset(self, offset):
        '''Find all intervals in dictionary stopping at `offset`:

        ::

            >>> a = TimeIntervalTree([TimeInterval(0, 1, {'name': 'a'})])
            >>> b = TimeIntervalTree([TimeInterval(1, 2, {'name': 'b'})])
            >>> c = TimeIntervalTree([TimeInterval(0, 3, {'name': 'c'})])
            >>> d = TimeIntervalTree([TimeInterval(2, 3, {'name': 'd'})])
            >>> treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})
            >>> treedict
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        ::

            >>> offset = 3
            >>> treedict.find_intervals_stopping_at_offset(offset)
            TimeIntervalTreeDictionary({
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        ::

            >>> offset = 1
            >>> treedict.find_intervals_stopping_at_offset(offset)
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
            })

        Return `TimeIntervalTreeDictionary` instance.
        '''

        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_stopping_at_offset(offset)
            if len(found):
                result[key] = found
        return type(self)(result)

    def find_intervals_stopping_before_offset(self, offset):
        '''Find all intervals in dictionary stopping before `offset`:

        ::

            >>> a = TimeIntervalTree([TimeInterval(0, 1, {'name': 'a'})])
            >>> b = TimeIntervalTree([TimeInterval(1, 2, {'name': 'b'})])
            >>> c = TimeIntervalTree([TimeInterval(0, 3, {'name': 'c'})])
            >>> d = TimeIntervalTree([TimeInterval(2, 3, {'name': 'd'})])
            >>> treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})
            >>> treedict
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        ::

            >>> offset = 3
            >>> treedict.find_intervals_stopping_before_offset(offset)
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
            })

        ::

            >>> offset = (7, 2)
            >>> treedict.find_intervals_stopping_before_offset(offset)
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        Return `TimeIntervalTreeDictionary` instance.
        '''

        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_stopping_before_offset(offset)
            if len(found):
                result[key] = found
        return type(self)(result)

    def find_intervals_stopping_within_interval(self, *args):
        '''Find all intervals in dictionary stopping within the interval 
        defined by `args`:

        ::

            >>> a = TimeIntervalTree([TimeInterval(0, 1, {'name': 'a'})])
            >>> b = TimeIntervalTree([TimeInterval(1, 2, {'name': 'b'})])
            >>> c = TimeIntervalTree([TimeInterval(0, 3, {'name': 'c'})])
            >>> d = TimeIntervalTree([TimeInterval(2, 3, {'name': 'd'})])
            >>> treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})
            >>> treedict
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        ::

            >>> interval = TimeInterval((3, 2), (5, 2))
            >>> treedict.find_intervals_stopping_within_interval(interval)
            TimeIntervalTreeDictionary({
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'b'}),
                ]),
            })

        ::

            >>> interval = TimeInterval((5, 2), (7, 2))
            >>> treedict.find_intervals_stopping_within_interval(interval)
            TimeIntervalTreeDictionary({
                'c': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(3, 1), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'd'}),
                ]),
            })

        Return `TimeIntervalTreeDictionary` instance.
        '''

        result = {}
        for key, tree in self.iteritems():
            found = tree.find_intervals_stopping_within_interval(*args)
            if len(found):
                result[key] = found
        return type(self)(result)

    def quantize_to_rational(self, rational):
        '''Quantize all intervals in dictionary to a multiple (1 or more) 
        of `rational`:

        ::

            >>> a = TimeIntervalTree([TimeInterval((1, 16), (1, 8), {'name': 'a'})])
            >>> b = TimeIntervalTree([TimeInterval((2, 7), (13, 7), {'name': 'b'})])
            >>> c = TimeIntervalTree([TimeInterval((3, 5), (8, 5), {'name': 'c'})])
            >>> d = TimeIntervalTree([TimeInterval((2, 3), (5, 3), {'name': 'd'})])
            >>> treedict = TimeIntervalTreeDictionary({'a': a, 'b': b, 'c': c, 'd': d})
            >>> treedict
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(1, 16), Offset(1, 8), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(2, 7), Offset(13, 7), {'name': 'b'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(3, 5), Offset(8, 5), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 3), Offset(5, 3), {'name': 'd'}),
                ]),
            })

        ::

            >>> rational = (1, 4)
            >>> treedict.quantize_to_rational(rational)
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 4), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 4), Offset(7, 4), {'name': 'b'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(1, 2), Offset(3, 2), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(3, 4), Offset(7, 4), {'name': 'd'}),
                ]),
            })

        ::

            >>> rational = (1, 3)
            >>> treedict.quantize_to_rational(rational)
            TimeIntervalTreeDictionary({
                'a': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 3), {'name': 'a'}),
                ]),
                'b': TimeIntervalTree([
                    TimeInterval(Offset(1, 3), Offset(2, 1), {'name': 'b'}),
                ]),
                'c': TimeIntervalTree([
                    TimeInterval(Offset(2, 3), Offset(5, 3), {'name': 'c'}),
                ]),
                'd': TimeIntervalTree([
                    TimeInterval(Offset(2, 3), Offset(5, 3), {'name': 'd'}),
                ]),
            })

        Return `TimeIntervalTreeDictionary` instance.
        '''

        rational = durationtools.Duration(rational)
        result = {}
        for key, tree in self.iteritems():
            result[key] = tree.quantize_to_rational(rational)
        return type(self)(result)

    def scale_by_rational(self, rational):
        '''Scale aggregate duration of dictionary by `rational`:

        ::

            >>> one = TimeIntervalTree([TimeInterval(0, 1, {'name': 'one'})])
            >>> two = TimeIntervalTree([TimeInterval((1, 2), (5, 2), {'name': 'two'})])
            >>> three = TimeIntervalTree([TimeInterval(2, 4, {'name': 'three'})])
            >>> treedict = TimeIntervalTreeDictionary(
            ...     {'one': one, 'two': two, 'three': three})
            >>> treedict
            TimeIntervalTreeDictionary({
                'one': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'one'}),
                ]),
                'three': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(4, 1), {'name': 'three'}),
                ]),
                'two': TimeIntervalTree([
                    TimeInterval(Offset(1, 2), Offset(5, 2), {'name': 'two'}),
                ]),
            })

        ::

            >>> result = treedict.scale_by_rational((2, 3))
            >>> result
            TimeIntervalTreeDictionary({
                'one': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(2, 3), {'name': 'one'}),
                ]),
                'three': TimeIntervalTree([
                    TimeInterval(Offset(4, 3), Offset(8, 3), {'name': 'three'}),
                ]),
                'two': TimeIntervalTree([
                    TimeInterval(Offset(1, 3), Offset(5, 3), {'name': 'two'}),
                ]),
            })

        Scaling works regardless of the starting offset of the 
        `TimeIntervalTreeDictionary`:

        ::

            >>> zero = TimeIntervalTree([TimeInterval(-4, 0, {'name': 'zero'})])
            >>> treedict = TimeIntervalTreeDictionary(
            ...     {'zero': zero, 'one': one, 'two': two, 'three': three})
            >>> treedict
            TimeIntervalTreeDictionary({
                'one': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'one'}),
                ]),
                'three': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(4, 1), {'name': 'three'}),
                ]),
                'two': TimeIntervalTree([
                    TimeInterval(Offset(1, 2), Offset(5, 2), {'name': 'two'}),
                ]),
                'zero': TimeIntervalTree([
                    TimeInterval(Offset(-4, 1), Offset(0, 1), {'name': 'zero'}),
                ]),
            })

        ::

            >>> result = treedict.scale_by_rational(2)
            >>> result
            TimeIntervalTreeDictionary({
                'one': TimeIntervalTree([
                    TimeInterval(Offset(4, 1), Offset(6, 1), {'name': 'one'}),
                ]),
                'three': TimeIntervalTree([
                    TimeInterval(Offset(8, 1), Offset(12, 1), {'name': 'three'}),
                ]),
                'two': TimeIntervalTree([
                    TimeInterval(Offset(5, 1), Offset(9, 1), {'name': 'two'}),
                ]),
                'zero': TimeIntervalTree([
                    TimeInterval(Offset(-4, 1), Offset(4, 1), {'name': 'zero'}),
                ]),
            })

        ::

            >>> result.start == treedict.start
            True
            >>> result.duration == treedict.duration * 2
            True

        Return `TimeIntervalTreeDictionary` instance.
        '''

        rational = durationtools.Duration(rational)
        result = {}
        for key, tree in self.iteritems():
            offset = (tree.start - self.start) * rational
            result[key] = tree.scale_by_rational(rational).shift_to_rational(self.start + offset)
        return type(self)(result)

    def scale_to_rational(self, rational):
        '''Scale aggregate duration of dictionary to `rational`:

        ::

            >>> one = TimeIntervalTree([TimeInterval(0, 1, {'name': 'one'})])
            >>> two = TimeIntervalTree([TimeInterval((1, 2), (5, 2), {'name': 'two'})])
            >>> three = TimeIntervalTree([TimeInterval(2, 4, {'name': 'three'})])
            >>> treedict = TimeIntervalTreeDictionary({'one': one, 'two': two, 'three': three})
            >>> treedict
            TimeIntervalTreeDictionary({
                'one': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'one'}),
                ]),
                'three': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(4, 1), {'name': 'three'}),
                ]),
                'two': TimeIntervalTree([
                    TimeInterval(Offset(1, 2), Offset(5, 2), {'name': 'two'}),
                ]),
            })

        ::

            >>> result = treedict.scale_to_rational(1)
            >>> result
            TimeIntervalTreeDictionary({
                'one': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 4), {'name': 'one'}),
                ]),
                'three': TimeIntervalTree([
                    TimeInterval(Offset(1, 2), Offset(1, 1), {'name': 'three'}),
                ]),
                'two': TimeIntervalTree([
                    TimeInterval(Offset(1, 8), Offset(5, 8), {'name': 'two'}),
                ]),
            })

        ::

            >>> result.scale_to_rational(10)
            TimeIntervalTreeDictionary({
                'one': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(5, 2), {'name': 'one'}),
                ]),
                'three': TimeIntervalTree([
                    TimeInterval(Offset(5, 1), Offset(10, 1), {'name': 'three'}),
                ]),
                'two': TimeIntervalTree([
                    TimeInterval(Offset(5, 4), Offset(25, 4), {'name': 'two'}),
                ]),
            })

        Scaling works regardless of the starting offset of the `TimeIntervalTreeDictionary`:

        ::

            >>> zero = TimeIntervalTree([TimeInterval(-4, 0, {'name': 'zero'})])
            >>> treedict = TimeIntervalTreeDictionary(
            ...     {'zero': zero, 'one': one, 'two': two, 'three': three})

        ::

            >>> treedict.scale_to_rational(4)
            TimeIntervalTreeDictionary({
                'one': TimeIntervalTree([
                    TimeInterval(Offset(-2, 1), Offset(-3, 2), {'name': 'one'}),
                ]),
                'three': TimeIntervalTree([
                    TimeInterval(Offset(-1, 1), Offset(0, 1), {'name': 'three'}),
                ]),
                'two': TimeIntervalTree([
                    TimeInterval(Offset(-7, 4), Offset(-3, 4), {'name': 'two'}),
                ]),
                'zero': TimeIntervalTree([
                    TimeInterval(Offset(-4, 1), Offset(-2, 1), {'name': 'zero'}),
                ]),
            })

        Return `TimeIntervalTreeDictionary` instance.
        '''

        rational = durationtools.Duration(rational)
        result = {}
        for key, tree in self.iteritems():
            offset = (((tree.start - self.start) / self.duration) * rational) + self.start
            duration = (tree.duration / self.duration) * rational
            result[key] = tree.scale_to_rational(duration).shift_to_rational(offset)
        return type(self)(result)

    def shift_by_rational(self, rational):
        '''Shift aggregate offset of dictionary by `rational`:

        ::

            >>> one = TimeIntervalTree([TimeInterval(0, 1, {'name': 'one'})])
            >>> two = TimeIntervalTree([TimeInterval((1, 2), (5, 2), {'name': 'two'})])
            >>> three = TimeIntervalTree([TimeInterval(2, 4, {'name': 'three'})])
            >>> treedict = TimeIntervalTreeDictionary({'one': one, 'two': two, 'three': three})
            >>> treedict
            TimeIntervalTreeDictionary({
                'one': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'one'}),
                ]),
                'three': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(4, 1), {'name': 'three'}),
                ]),
                'two': TimeIntervalTree([
                    TimeInterval(Offset(1, 2), Offset(5, 2), {'name': 'two'}),
                ]),
            })

        ::

            >>> result = treedict.shift_by_rational(-2.5)
            >>> result
            TimeIntervalTreeDictionary({
                'one': TimeIntervalTree([
                    TimeInterval(Offset(-5, 2), Offset(-3, 2), {'name': 'one'}),
                ]),
                'three': TimeIntervalTree([
                    TimeInterval(Offset(-1, 2), Offset(3, 2), {'name': 'three'}),
                ]),
                'two': TimeIntervalTree([
                    TimeInterval(Offset(-2, 1), Offset(0, 1), {'name': 'two'}),
                ]),
            })

        ::

            >>> result.shift_by_rational(6)
            TimeIntervalTreeDictionary({
                'one': TimeIntervalTree([
                    TimeInterval(Offset(7, 2), Offset(9, 2), {'name': 'one'}),
                ]),
                'three': TimeIntervalTree([
                    TimeInterval(Offset(11, 2), Offset(15, 2), {'name': 'three'}),
                ]),
                'two': TimeIntervalTree([
                    TimeInterval(Offset(4, 1), Offset(6, 1), {'name': 'two'}),
                ]),
            })

        Return `TimeIntervalTreeDictionary` instance.
        '''

        rational = durationtools.Offset(rational)
        result = {}
        for key, tree in self.iteritems():
            result[key] = tree.shift_by_rational(rational)
        return type(self)(result)

    def shift_to_rational(self, rational):
        '''Shift aggregate offset of dictionary to `rational`:

        ::

            >>> one = TimeIntervalTree([TimeInterval(0, 1, {'name': 'one'})])
            >>> two = TimeIntervalTree([TimeInterval((1, 2), (5, 2), {'name': 'two'})])
            >>> three = TimeIntervalTree([TimeInterval(2, 4, {'name': 'three'})])
            >>> treedict = TimeIntervalTreeDictionary({'one': one, 'two': two, 'three': three})
            >>> treedict
            TimeIntervalTreeDictionary({
                'one': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'one'}),
                ]),
                'three': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(4, 1), {'name': 'three'}),
                ]),
                'two': TimeIntervalTree([
                    TimeInterval(Offset(1, 2), Offset(5, 2), {'name': 'two'}),
                ]),
            })

        ::

            >>> result = treedict.shift_to_rational(100)
            >>> result
            TimeIntervalTreeDictionary({
                'one': TimeIntervalTree([
                    TimeInterval(Offset(100, 1), Offset(101, 1), {'name': 'one'}),
                ]),
                'three': TimeIntervalTree([
                    TimeInterval(Offset(102, 1), Offset(104, 1), {'name': 'three'}),
                ]),
                'two': TimeIntervalTree([
                    TimeInterval(Offset(201, 2), Offset(205, 2), {'name': 'two'}),
                ]),
            })

        Return `TimeIntervalTreeDictionary` instance.
        '''

        rational = durationtools.Offset(rational)
        result = {}
        for key, tree in self.iteritems():
            offset = tree.start - self.start
            result[key] = tree.shift_to_rational(rational + offset)
        return type(self)(result)

    def split_at_rationals(self, *rationals):
        '''Split dictionary at each rational in `rationals`:

        ::

            >>> one = TimeIntervalTree([TimeInterval(0, 1, {'name': 'one'})])
            >>> two = TimeIntervalTree([TimeInterval((1, 2), (5, 2), {'name': 'two'})])
            >>> three = TimeIntervalTree([TimeInterval(2, 4, {'name': 'three'})])
            >>> treedict = TimeIntervalTreeDictionary({'one': one, 'two': two, 'three': three})
            >>> treedict
            TimeIntervalTreeDictionary({
                'one': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'one'}),
                ]),
                'three': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(4, 1), {'name': 'three'}),
                ]),
                'two': TimeIntervalTree([
                    TimeInterval(Offset(1, 2), Offset(5, 2), {'name': 'two'}),
                ]),
            })

        ::

            >>> result = treedict.split_at_rationals(1, 2, 3)
            >>> len(result)
            4

        ::

            >>> result[0]
            TimeIntervalTreeDictionary({
                'one': TimeIntervalTree([
                    TimeInterval(Offset(0, 1), Offset(1, 1), {'name': 'one'}),
                ]),
                'two': TimeIntervalTree([
                    TimeInterval(Offset(1, 2), Offset(1, 1), {'name': 'two'}),
                ]),
            })

        ::

            >>> result[1]
            TimeIntervalTreeDictionary({
                'two': TimeIntervalTree([
                    TimeInterval(Offset(1, 1), Offset(2, 1), {'name': 'two'}),
                ]),
            })

        ::

            >>> result[2]
            TimeIntervalTreeDictionary({
                'three': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(3, 1), {'name': 'three'}),
                ]),
                'two': TimeIntervalTree([
                    TimeInterval(Offset(2, 1), Offset(5, 2), {'name': 'two'}),
                ]),
            })

        ::

            >>> result[3]
            TimeIntervalTreeDictionary({
                'three': TimeIntervalTree([
                    TimeInterval(Offset(3, 1), Offset(4, 1), {'name': 'three'}),
                ]),
            })

        Return tuple of `TimeIntervalTreeDictionary` instances.
        '''

        assert 0 < len(rationals)
        rationals = sorted([durationtools.Offset(x) for x in rationals])
        rationals = [x for x in rationals if self.start < x < self.stop]
        dicts = []
        carried = dict(self)
        to_remove = []
        for rational in rationals:
            result = {}
            for key, tree in carried.iteritems():
                if tree is None:
                    continue
                splits = tree.split_at_rationals(rational)
                if len(splits) == 2:
                    result[key] = splits[0]
                    carried[key] = splits[1]
                elif splits[0].stop <= rational:
                    result[key] = splits[0]
                    carried[key] = None
                    to_remove.append(key)
                elif rational <= splits[0].start:
                    pass
                else:
                    raise Exception('Tree failed to split.')
            if result:
                dicts.append(type(self)(result))
        for key in to_remove:
            del(carried[key])
        if carried:
            dicts.append(type(self)(carried))
        return tuple(dicts)
