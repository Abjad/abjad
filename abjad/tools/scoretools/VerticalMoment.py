import collections
from abjad.tools import abctools


class VerticalMoment(abctools.AbjadObject):
    r'''Vertical moment.

    ..  container:: example

        >>> score = abjad.Score()
        >>> staff_group = abjad.StaffGroup()
        >>> staff_group.context_name = 'PianoStaff'
        >>> staff_group.append(abjad.Staff("c'4 e'4 d'4 f'4"))
        >>> staff_group.append(abjad.Staff(r"""\clef "bass" g2 f2"""))
        >>> score.append(staff_group)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
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

        >>> for moment in abjad.iterate(score).vertical_moments():
        ...     moment
        ...
        VerticalMoment(0, <<2>>)
        VerticalMoment(1/4, <<2>>)
        VerticalMoment(1/2, <<2>>)
        VerticalMoment(3/4, <<2>>)

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Selections'

    __slots__ = (
        '_components',
        '_governors',
        '_offset',
        )

    ### INITIALIZER ###

    def __init__(self, components=None, offset=None):
        import abjad
        if components is None:
            self._offset = offset
            self._components = ()
            self._governors = ()
        else:
            governors, components = self._from_offset(components, offset)
            offset = abjad.Offset(offset)
            self._offset = offset
            assert isinstance(governors, collections.Iterable)
            governors = tuple(governors)
            self._governors = governors
            assert isinstance(components, collections.Iterable)
            components = list(components)
            components.sort(
                key=lambda _: abjad.inspect(_).get_parentage().score_index)
        self._components = components

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when `argument` is a vertical moment with the same
        components as this vertical moment. Otherwise false.

        Returns true or false.
        '''
        if isinstance(argument, VerticalMoment):
            if len(self) == len(argument):
                for c, d in zip(self.components, argument.components):
                    if c is not d:
                        return False
                else:
                    return True
        return False

    # redefined because of custom __eq__()
    def __hash__(self):
        r'''Hases vertical moment.

        Returns integer.
        '''
        if self.components:
            return hash(tuple([id(_) for _ in self.components]))
        return 0

    def __len__(self):
        r'''Length of vertical moment.

        Defined equal to the number of components in vertical moment.

        Returns nonnegative integer.
        '''
        return len(self.components)

    def __repr__(self):
        r'''Gets interpreter representation of vertical moment.

        Returns string.
        '''
        if not self.components:
            return '{}()'.format(type(self).__name__)
        result = '{}({}, <<{}>>)'
        result = result.format(
            type(self).__name__,
            str(self.offset),
            len(self.leaves),
            )
        return result

    ### PRIVATE METHODS ###

    @staticmethod
    def _find_index(container, offset):
        r'''Based off of Python's bisect.bisect() function.
        '''
        import abjad
        lo = 0
        hi = len(container)
        while lo < hi:
            mid = (lo + hi) // 2
            start_offset = abjad.inspect(container[mid]).get_timespan().start_offset
            stop_offset = abjad.inspect(container[mid]).get_timespan().stop_offset
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
    def _from_offset(argument, offset):
        import abjad
        offset = abjad.Offset(offset)
        governors = []
        prototype = (list, tuple, abjad.Selection)
        message = 'must be component or of Abjad components: {!r}.'
        message = message.format(argument)
        if isinstance(argument, abjad.Component):
            governors.append(argument)
        elif isinstance(argument, prototype):
            for x in argument:
                if isinstance(x, sabjad.Component):
                    governors.append(x)
                else:
                    raise TypeError(message)
        else:
            raise TypeError(message)
        governors.sort(
            key=lambda x: abjad.inspect(x).get_parentage().score_index)
        governors = tuple(governors)
        components = []
        for governor in governors:
            components.extend(VerticalMoment._recurse(governor, offset))
        components.sort(
            key=lambda x: abjad.inspect(x).get_parentage().score_index)
        components = tuple(components)
        return governors, components

    def _get_format_specification(self):
        import abjad
        return abjad.FormatSpecification(client=self)

    @staticmethod
    def _recurse(component, offset):
        import abjad
        result = []
        if (abjad.inspect(component).get_timespan().start_offset <=
            offset < abjad.inspect(component).get_timespan().stop_offset):
            result.append(component)
            if hasattr(component, 'components'):
                if component.is_simultaneous:
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
        r'''Positive integer number of pitch carriers starting at vertical
        moment.
        '''
        import abjad
        attack_carriers = []
        for leaf in self.start_leaves:
            if isinstance(leaf, (abjad.Note, abjad.Chord)):
                attack_carriers.append(leaf)
        return len(attack_carriers)

    @property
    def components(self):
        r'''Tuple of zero or more components happening at vertical moment.

        It is always the case that ``self.components =
        self.overlap_components + self.start_components``.
        '''
        return self._components

    @property
    def governors(self):
        r'''Tuple of one or more containers in which vertical moment is
        evaluated.
        '''
        return self._governors

    @property
    def leaves(self):
        r'''Tuple of zero or more leaves at vertical moment.
        '''
        import abjad
        result = []
        for component in self.components:
            if isinstance(component, abjad.Leaf):
                result.append(component)
        result = abjad.select(result)
        return result

    @property
    def measures(self):
        r'''Tuplet of zero or more measures at vertical moment.
        '''
        import abjad
        result = []
        for component in self.components:
            if isinstance(component, abjad.Measure):
                result.append(component)
        result = tuple(result)
        return result

    @property
    def next_vertical_moment(self):
        r'''Reference to next vertical moment forward in time.
        '''
        import abjad
        candidate_shortest_leaf = self.leaves[0]
        for leaf in self.leaves[1:]:
            if (abjad.inspect(leaf).get_timespan().stop_offset <
                abjad.inspect(candidate_shortest_leaf).get_timespan().stop_offset):
                candidate_shortest_leaf = leaf
        next_leaf = candidate_shortest_leaf._get_in_my_logical_voice(
            1, prototype=abjad.Leaf)
        next_vertical_moment = next_leaf._get_vertical_moment()
        return next_vertical_moment

    @property
    def notes(self):
        r'''Tuple of zero or more notes at vertical moment.
        '''
        import abjad
        result = []
        prototype = (abjad.Note,)
        for component in self.components:
            if isinstance(component, prototype):
                result.append(component)
        result = tuple(result)
        return result

    @property
    def notes_and_chords(self):
        r'''Tuple of zero or more notes and chords at vertical moment.
        '''
        import abjad
        result = []
        prototype = (abjad.Chord, abjad.Note)
        for component in self.components:
            if isinstance(component, prototype):
                result.append(component)
        result = tuple(result)
        return result

    @property
    def offset(self):
        r'''Rational-valued score offset at which vertical moment is evaluated.
        '''
        return self._offset

    @property
    def overlap_components(self):
        r'''Tuple of components in vertical moment starting before vertical
        moment, ordered by score index.
        '''
        result = []
        for component in self.components:
            if component.start < self.offset:
                result.append(component)
        result = tuple(result)
        return result

    @property
    def overlap_leaves(self):
        r'''Tuple of leaves in vertical moment starting before vertical moment,
        ordered by score index.
        '''
        import abjad
        result = [x for x in self.overlap_components
            if isinstance(x, abjad.Leaf)]
        result = tuple(result)
        return result

    @property
    def overlap_measures(self):
        r'''Tuple of measures in vertical moment starting before vertical
        moment, ordered by score index.
        '''
        import abjad
        result = self.overlap_components
        result = [_ for _ in result if isinstance(_, abjad.Measure)]
        result = tuple(result)
        return result

    @property
    def overlap_notes(self):
        r'''Tuple of notes in vertical moment starting before vertical moment,
        ordered by score index.
        '''
        import abjad
        result = self.overlap_components
        result = [_ for _ in result if isinstance(_, abjad.Note)]
        result = tuple(result)
        return result

    @property
    def previous_vertical_moment(self):
        r'''Reference to previous vertical moment backward in time.
        '''
        import abjad
        if self.offset == 0:
            raise IndexError
        most_recent_start_offset = abjad.Offset(0)
        token_leaf = None
        for leaf in self.leaves:
            #print ''
            #print leaf
            leaf_start = abjad.inspect(leaf).get_timespan().start_offset
            if leaf_start < self.offset:
                #print 'found leaf starting before this moment ...'
                if most_recent_start_offset <= leaf_start:
                    most_recent_start_offset = leaf_start
                    token_leaf = leaf
            else:
                #print 'found leaf starting on this moment ...'
                try:
                    previous_leaf = leaf._get_in_my_logical_voice(
                        -1, prototype=abjad.Leaf)
                    start = abjad.inspect(previous_leaf).get_timespan().start_offset
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
        previous_vertical_moment = token_leaf._get_vertical_moment()
        return previous_vertical_moment

    @property
    def start_components(self):
        r'''Tuple of components in vertical moment starting with at vertical
        moment, ordered by score index.
        '''
        import abjad
        result = []
        for component in self.components:
            if abjad.inspect(
                component).get_timespan().start_offset == self.offset:
                result.append(component)
        result = tuple(result)
        return result

    @property
    def start_leaves(self):
        r'''Tuple of leaves in vertical moment starting with vertical moment,
        ordered by score index.
        '''
        import abjad
        result = [x for x in self.start_components
            if isinstance(x, abjad.Leaf)]
        result = tuple(result)
        return result

    @property
    def start_notes(self):
        r'''Tuple of notes in vertical moment starting with vertical moment,
        ordered by score index.
        '''
        import abjad
        result = [x for x in self.start_components
            if isinstance(x, abjad.Note)]
        result = tuple(result)
        return result


collections.Sequence.register(VerticalMoment)
