from abjad.tools import componenttools
from abjad.tools import chordtools
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import measuretools
from abjad.tools import notetools
from abjad.tools.abctools import ScoreSelection


class VerticalMoment(ScoreSelection):
    r'''.. versionadded: 1.1.2

    Everything happening at a single moment in musical time::

        >>> from abjad.tools import verticalitytools

    ::

        >>> score = Score([])
        >>> piano_staff = scoretools.PianoStaff([])
        >>> piano_staff.append(Staff("c'4 e'4 d'4 f'4"))
        >>> piano_staff.append(Staff(r"""\clef "bass" g2 f2"""))
        >>> score.append(piano_staff)

    ::

        f(score)
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

        >>> for x in verticalitytools.iterate_vertical_moments_in_expr(score):
        ...     x
        ...
        VerticalMoment(0, <<2>>)
        VerticalMoment(1/4, <<2>>)
        VerticalMoment(1/2, <<2>>)
        VerticalMoment(3/4, <<2>>)

    Create vertical moments with the getters and iterators implemented in 
    the ``verticalitytools`` module.

    Vertical moments are immutable.
    '''

    ### CLASS ATTRIBUTES ###
    
    __slots__ = ('_components', '_governors', '_prolated_offset')

    ### INITIALIZER ###

    def __init__(self, prolated_offset, governors, components):
        prolated_offset = durationtools.Offset(prolated_offset)
        assert isinstance(governors, tuple)
        assert isinstance(components, tuple)
        object.__setattr__(self, '_prolated_offset', prolated_offset)
        object.__setattr__(self, '_governors', tuple(governors))
        components = list(components)
        components.sort(
            lambda x, y: cmp(
            componenttools.component_to_score_index(x),
            componenttools.component_to_score_index(y)))
        object.__setattr__(self, '_components', tuple(components))

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
        result.append(str(self.prolated_offset))
        result.extend([str(id(x)) for x in self.governors])
        result = '+'.join(result)
        return hash(repr(result))

    def __len__(self):
        return len(self.components)

    def __ne__(self, expr):
        return not self == expr

    def __repr__(self):
        return '%s(%s, <<%s>>)' % (type(self).__name__, self.prolated_offset, len(self.leaves))

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return ', '.join([str(x) for x in self.components])

    ### PUBLIC PROPERTIES ###

    @property
    def attack_count(self):
        '''Positive integer number of pitch carriers
        starting at vertical moment.'''
        attack_carriers = []
        for leaf in self.start_leaves:
            if isinstance(leaf, (notetools.Note, chordtools.Chord)):
                attack_carriers.append(leaf)
        return len(attack_carriers)

    @property
    def components(self):
        '''Read-only tuple of zero or more components
        happening at vertical moment.

        It is always the case that ``self.components =
        self.overlap_components + self.start_components``.'''
        return self._components

    @property
    def governors(self):
        '''Read-only tuple of one or more containers
        in which vertical moment is evaluated.'''
        return self._governors

    @property
    def leaves(self):
        '''Read-only tuple of zero or more leaves
        at vertical moment.'''
        result = []
        for component in self.components:
            if isinstance(component, leaftools.Leaf):
                result.append(component)
        result = tuple(result)
        return result

    @property
    def measures(self):
        '''Read-only tuplet of zero or more measures
        at vertical moment.'''
        result = []
        for component in self.components:
            if isinstance(component, measuretools.Measure):
                result.append(component)
        result = tuple(result)
        return result

    @property
    def next_vertical_moment(self):
        '''Read-only reference to next vertical moment forward in time.'''
        from abjad.tools import verticalitytools
        candidate_shortest_leaf = self.leaves[0]
        for leaf in self.leaves[1:]:
            if leaf.stop < candidate_shortest_leaf.stop:
                candidate_shortest_leaf = leaf
        next_leaf = componenttools.get_nth_namesake_from_component(candidate_shortest_leaf, 1)
        next_vertical_moment = verticalitytools.get_vertical_moment_starting_with_component(next_leaf)
        return next_vertical_moment

    @property
    def next_vertical_moment(self):
        '''Read-only reference to next vertical moment forward in time.'''
        from abjad.tools import verticalitytools
        candidate_shortest_leaf = self.leaves[0]
        for leaf in self.leaves[1:]:
            if leaf.stop_offset < candidate_shortest_leaf.stop_offset:
                candidate_shortest_leaf = leaf
        next_leaf = componenttools.get_nth_namesake_from_component(candidate_shortest_leaf, 1)
        next_vertical_moment = verticalitytools.get_vertical_moment_starting_with_component(
            next_leaf)
        return next_vertical_moment

    @property
    def notes(self):
        '''Read-only tuple of zero or more notes
        at vertical moment.'''
        result = []
        for component in self.components:
            if isinstance(component, notetools.Note):
                result.append(component)
        result = tuple(result)
        return result

    @property
    def overlap_components(self):
        '''Read-only tuple of components in vertical moment
        starting before vertical moment, ordered by score index.'''
        result = []
        for component in self.components:
            if component.start < self.prolated_offset:
                result.append(component)
        result = tuple(result)
        return result

    @property
    def overlap_leaves(self):
        '''Read-only tuple of leaves in vertical moment
        starting before vertical moment, ordered by score index.'''
        result = [x for x in self.overlap_components if isinstance(x, leaftools.Leaf)]
        result = tuple(result)
        return result

    @property
    def overlap_measures(self):
        '''Read-only tuple of measures in vertical moment
        starting before vertical moment, ordered by score index.'''
        result = [x for x in self.overlap_components if isinstance(x, measuretools.Measure)]
        result = tuple(result)
        return result

    @property
    def overlap_notes(self):
        '''Read-only tuple of notes in vertical moment
        starting before vertical moment, ordered by score index.'''
        result = [x for x in self.overlap_components if isinstance(x, notetools.Note)]
        result = tuple(result)
        return result

    @property
    def prev_vertical_moment(self):
        '''Read-only reference to prev vertical moment backward in time.'''
        from abjad.tools import verticalitytools
        if self.prolated_offset == 0:
            raise IndexError
        most_recent_start_offset = durationtools.Offset(0)
        token_leaf = None
        for leaf in self.leaves:
            #print ''
            #print leaf
            leaf_start = leaf.start_offset
            if leaf_start < self.prolated_offset:
                #print 'found leaf starting before this moment ...'
                if most_recent_start_offset <= leaf_start:
                    most_recent_start_offset = leaf_start
                    token_leaf = leaf
            else:
                #print 'found leaf starting on this moment ...'
                try:
                    prev_leaf = componenttools.get_nth_namesake_from_component(leaf, -1)
                    start = prev_leaf.start_offset
                    #print prev_leaf, start
                    if most_recent_start_offset <= start:
                        most_recent_start_offset = start
                        token_leaf = prev_leaf
                except IndexError:
                    pass
        #print 'token_leaf is %s ...' % token_leaf
        if token_leaf is None:
            token_leaf = leaf
            #print 'token_leaf is %s ...' % token_leaf
        prev_vertical_moment = verticalitytools.get_vertical_moment_starting_with_component(
            token_leaf)
        return prev_vertical_moment

    @property
    def prolated_offset(self):
        '''Read-only rational-valued score offset
        at which vertical moment is evaluated.'''
        return self._prolated_offset

    @property
    def start_components(self):
        '''Read-only tuple of components in vertical moment
        starting with at vertical moment, ordered by score index.'''
        result = []
        for component in self.components:
            if component.start_offset == self.prolated_offset:
                result.append(component)
        result = tuple(result)
        return result

    @property
    def start_leaves(self):
        '''Read-only tuple of leaves in vertical moment
        starting with vertical moment, ordered by score index.'''
        result = [x for x in self.start_components if isinstance(x, leaftools.Leaf)]
        result = tuple(result)
        return result

    @property
    def start_notes(self):
        '''Read-only tuple of notes in vertical moment
        starting with vertical moment, ordered by score index.'''
        result = [x for x in self.start_components if isinstance(x, notetools.Note)]
        result = tuple(result)
        return result
