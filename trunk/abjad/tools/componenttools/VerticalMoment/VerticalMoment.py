from abjad.tools import durationtools
from abjad.tools.selectiontools import SimultaneousSelection


class VerticalMoment(SimultaneousSelection):
    r'''Everything happening at a single moment in musical time:

    ::

        >>> score = Score([])
        >>> piano_staff = scoretools.PianoStaff([])
        >>> piano_staff.append(Staff("c'4 e'4 d'4 f'4"))
        >>> piano_staff.append(Staff(r"""\clef "bass" g2 f2"""))
        >>> score.append(piano_staff)

    ::

        >>> f(score)
        \new Score <<
            \new PianoStaff <<
                \new Staff {
                    c'4
                    e'4
                    d'4
                    f'4
                }
                \new Staff {
                    \clef "bass"
                    g2
                    f2
                }
            >>
        >>

    ::

        >>> show(score) # doctest: +SKIP

    ::

        >>> for x in iterationtools.iterate_vertical_moments_in_expr(score):
        ...     x
        ...
        VerticalMoment(0, <<2>>)
        VerticalMoment(1/4, <<2>>)
        VerticalMoment(1/2, <<2>>)
        VerticalMoment(3/4, <<2>>)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_components',
        '_governors',
        '_offset',
        )

    ### INITIALIZER ###

    def __init__(self, expr=None, offset=None):
        if expr is None:
            return
        governors, components = self._from_expr_and_offset(expr, offset)
        offset = durationtools.Offset(offset)
        assert isinstance(governors, tuple)
        assert isinstance(components, tuple)
        self._offset = offset
        self._governors = tuple(governors)
        components = list(components)
        components.sort(key=lambda x: x.select_parentage().score_index)
        self._components = tuple(components)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, VerticalMoment):
            if len(self) == len(expr):
                for c, d in zip(self.components, expr.components):
                    if c is not d:
                        return False
                else:
                    return True
        return False

    def __hash__(self):
        result = []
        result.append(str(self.offset))
        result.extend([str(id(x)) for x in self.governors])
        result = '+'.join(result)
        return hash(repr(result))

    def __len__(self):
        return len(self.components)

    def __ne__(self, expr):
        return not self == expr

    def __repr__(self):
        return '%s(%s, <<%s>>)' % (
            self.__class__.__name__,
            self.offset,
            len(self.leaves),
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return ', '.join([str(x) for x in self.components])

    ### PRIVATE METHODS ###

    @staticmethod
    def _find_index(container, offset):
        '''Based off of Python's bisect.bisect() function.
        '''
        lo = 0
        hi = len(container)
        while lo < hi:
            mid = (lo + hi) // 2
            start_offset = container[mid].timespan.start_offset
            stop_offset = container[mid].timespan.stop_offset
            if start_offset <= offset < stop_offset:
                lo = mid + 1
            # if container[mid] is of nonzero duration
            elif start_offset < stop_offset:
                hi = mid
            # container[mid] is of zero duration so we skip it
            else:
                lo = mid + 1
        return lo - 1

    @staticmethod
    def _from_expr_and_offset(expr, offset):
        from abjad.tools import componenttools
        from abjad.tools import selectiontools
        offset = durationtools.Offset(offset)
        governors = []
        if isinstance(expr, componenttools.Component):
            governors.append(expr)
        elif isinstance(expr, (list, tuple, selectiontools.SequentialSelection)):
            for x in expr:
                if isinstance(x, componenttools.Component):
                    governors.append(x)
                else:
                    message = 'must be Abjad component'
                    message += ' or tuple of Abjad components.'
                    raise TypeError(message)
        else:
            raise TypeError(message)
        governors.sort(key=lambda x: x.select_parentage().score_index)
        governors = tuple(governors)
        components = []
        for governor in governors:
            components.extend(VerticalMoment._recurse(governor, offset))
        components.sort(key=lambda x: x.select_parentage().score_index)
        components = tuple(components)
        return governors, components

    @staticmethod
    def _recurse(component, offset):
        result = []
        if component.timespan.start_offset <= \
            offset < component.timespan.stop_offset:
            result.append(component)
            if hasattr(component, '_music'):
                if component.is_parallel:
                    for x in component:
                        result.extend(VerticalMoment._recurse(x, offset))
                else:
                    child = component[
                        VerticalMoment._find_index(component, offset)]
                    result.extend(VerticalMoment._recurse(child, offset))
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def attack_count(self):
        '''Positive integer number of pitch carriers
        starting at vertical moment.
        '''
        from abjad.tools import chordtools
        from abjad.tools import notetools
        attack_carriers = []
        for leaf in self.start_leaves:
            if isinstance(leaf, (notetools.Note, chordtools.Chord)):
                attack_carriers.append(leaf)
        return len(attack_carriers)

    @property
    def components(self):
        '''Tuple of zero or more components
        happening at vertical moment.

        It is always the case that ``self.components =
        self.overlap_components + self.start_components``.
        '''
        return self._components

    @property
    def governors(self):
        '''Tuple of one or more containers
        in which vertical moment is evaluated.
        '''
        return self._governors

    @property
    def leaves(self):
        '''Tuple of zero or more leaves
        at vertical moment.
        '''
        from abjad.tools import leaftools
        result = []
        for component in self.components:
            if isinstance(component, leaftools.Leaf):
                result.append(component)
        result = tuple(result)
        return result

    @property
    def measures(self):
        '''Tuplet of zero or more measures
        at vertical moment.
        '''
        from abjad.tools import measuretools
        result = []
        for component in self.components:
            if isinstance(component, measuretools.Measure):
                result.append(component)
        result = tuple(result)
        return result

    @property
    def next_vertical_moment(self):
        '''Reference to next vertical moment forward in time.
        '''
        from abjad.tools import componenttools
        candidate_shortest_leaf = self.leaves[0]
        for leaf in self.leaves[1:]:
            if leaf.stop < candidate_shortest_leaf.stop:
                candidate_shortest_leaf = leaf
        next_leaf = candidate_shortest_leaf._get_namesake(1)
        next_vertical_moment = next_leaf.select_vertical_moment()
        return next_vertical_moment

    @property
    def next_vertical_moment(self):
        '''Reference to next vertical moment forward in time.
        '''
        from abjad.tools import componenttools
        candidate_shortest_leaf = self.leaves[0]
        for leaf in self.leaves[1:]:
            if leaf.timespan.stop_offset < \
                candidate_shortest_leaf.timespan.stop_offset:
                candidate_shortest_leaf = leaf
        next_leaf = candidate_shortest_leaf._get_namesake(1)
        next_vertical_moment = next_leaf.select_vertical_moment()
        return next_vertical_moment

    @property
    def notes(self):
        '''Tuple of zero or more notes
        at vertical moment.
        '''
        from abjad.tools import notetools
        result = []
        for component in self.components:
            if isinstance(component, notetools.Note):
                result.append(component)
        result = tuple(result)
        return result

    @property
    def offset(self):
        '''Rational-valued score offset
        at which vertical moment is evaluated.
        '''
        return self._offset

    @property
    def overlap_components(self):
        '''Tuple of components in vertical moment
        starting before vertical moment, ordered by score index.
        '''
        result = []
        for component in self.components:
            if component.start < self.offset:
                result.append(component)
        result = tuple(result)
        return result

    @property
    def overlap_leaves(self):
        '''Tuple of leaves in vertical moment
        starting before vertical moment, ordered by score index.
        '''
        from abjad.tools import leaftools
        result = [x for x in self.overlap_components 
            if isinstance(x, leaftools.Leaf)]
        result = tuple(result)
        return result

    @property
    def overlap_measures(self):
        '''Tuple of measures in vertical moment
        starting before vertical moment, ordered by score index.
        '''
        from abjad.tools import measuretools
        result = [x for x in self.overlap_components 
            if isinstance(x, measuretools.Measure)]
        result = tuple(result)
        return result

    @property
    def overlap_notes(self):
        '''Tuple of notes in vertical moment
        starting before vertical moment, ordered by score index.
        '''
        from abjad.tools import notetools
        result = [x for x in self.overlap_components 
            if isinstance(x, notetools.Note)]
        result = tuple(result)
        return result

    @property
    def previous_vertical_moment(self):
        '''Reference to prev vertical moment backward in time.
        '''
        from abjad.tools import componenttools
        if self.offset == 0:
            raise IndexError
        most_recent_start_offset = durationtools.Offset(0)
        token_leaf = None
        for leaf in self.leaves:
            #print ''
            #print leaf
            leaf_start = leaf.timespan.start_offset
            if leaf_start < self.offset:
                #print 'found leaf starting before this moment ...'
                if most_recent_start_offset <= leaf_start:
                    most_recent_start_offset = leaf_start
                    token_leaf = leaf
            else:
                #print 'found leaf starting on this moment ...'
                try:
                    previous_leaf = leaf._get_namesake(-1)
                    start = previous_leaf.timespan.start_offset
                    #print previous_leaf, start
                    if most_recent_start_offset <= start:
                        most_recent_start_offset = start
                        token_leaf = previous_leaf
                except IndexError:
                    pass
        #print 'token_leaf is %s ...' % token_leaf
        if token_leaf is None:
            token_leaf = leaf
            #print 'token_leaf is %s ...' % token_leaf
        previous_vertical_moment = token_leaf.select_vertical_moment()
        return previous_vertical_moment

    @property
    def start_components(self):
        '''Tuple of components in vertical moment
        starting with at vertical moment, ordered by score index.
        '''
        result = []
        for component in self.components:
            if component.timespan.start_offset == self.offset:
                result.append(component)
        result = tuple(result)
        return result

    @property
    def start_leaves(self):
        '''Tuple of leaves in vertical moment
        starting with vertical moment, ordered by score index.
        '''
        from abjad.tools import leaftools
        result = [x for x in self.start_components 
            if isinstance(x, leaftools.Leaf)]
        result = tuple(result)
        return result

    @property
    def start_notes(self):
        '''Tuple of notes in vertical moment
        starting with vertical moment, ordered by score index.
        '''
        from abjad.tools import notetools
        result = [x for x in self.start_components 
            if isinstance(x, notetools.Note)]
        result = tuple(result)
        return result
