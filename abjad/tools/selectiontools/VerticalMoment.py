# -*- coding: utf-8 -*-
import collections
from abjad.tools import durationtools
from abjad.tools import systemtools
from abjad.tools.selectiontools.Selection import Selection


class VerticalMoment(Selection):
    r'''Vertical moment of a component.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> score = abjad.Score()
            >>> staff_group = abjad.StaffGroup()
            >>> staff_group.context_name = 'PianoStaff'
            >>> staff_group.append(abjad.Staff("c'4 e'4 d'4 f'4"))
            >>> staff_group.append(abjad.Staff(r"""\clef "bass" g2 f2"""))
            >>> score.append(staff_group)
            >>> show(score) # doctest: +SKIP

        ..  docs::

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

            >>> for moment in abjad.iterate(score).by_vertical_moment():
            ...     moment
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

    def __init__(self, music=None, offset=None):
        self._music = music
        if music is None:
            self._offset = offset
            self._components = ()
            self._governors = ()
            return
        governors, components = self._from_offset(music, offset)
        offset = durationtools.Offset(offset)
        self._offset = offset
        assert isinstance(governors, collections.Iterable)
        governors = tuple(governors)
        self._governors = governors
        assert isinstance(components, collections.Iterable)
        components = list(components)
        components.sort(key=lambda _: _._get_parentage().score_index)
        self._components = tuple(components)

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

    def __hash__(self):
        r'''Hases vertical moment.

        Returns integer.
        '''
        return super(VerticalMoment, self).__hash__()

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
        lo = 0
        hi = len(container)
        while lo < hi:
            mid = (lo + hi) // 2
            start_offset = container[mid]._get_timespan().start_offset
            stop_offset = container[mid]._get_timespan().stop_offset
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
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        offset = durationtools.Offset(offset)
        governors = []
        prototype = (list, tuple, selectiontools.Selection)
        message = 'must be component or of Abjad components: {!r}.'
        message = message.format(argument)
        if isinstance(argument, scoretools.Component):
            governors.append(argument)
        elif isinstance(argument, prototype):
            for x in argument:
                if isinstance(x, scoretools.Component):
                    governors.append(x)
                else:
                    raise TypeError(message)
        else:
            raise TypeError(message)
        governors.sort(key=lambda x: x._get_parentage().score_index)
        governors = tuple(governors)
        components = []
        for governor in governors:
            components.extend(VerticalMoment._recurse(governor, offset))
        components.sort(key=lambda x: x._get_parentage().score_index)
        components = tuple(components)
        return governors, components

    def _get_format_specification(self):
        return systemtools.FormatSpecification(client=self)

    @staticmethod
    def _recurse(component, offset):
        result = []
        if (component._get_timespan().start_offset <=
            offset < component._get_timespan().stop_offset):
            result.append(component)
            if hasattr(component, '_music'):
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
        from abjad.tools import scoretools
        attack_carriers = []
        for leaf in self.start_leaves:
            if isinstance(leaf, (scoretools.Note, scoretools.Chord)):
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
        from abjad.tools import scoretools
        result = []
        for component in self.components:
            if isinstance(component, scoretools.Measure):
                result.append(component)
        result = tuple(result)
        return result

    @property
    def music(self):
        r'''Gets music of vertical moment.

        Returns component or selection.
        '''
        return self._music

    @property
    def next_vertical_moment(self):
        r'''Reference to next vertical moment forward in time.
        '''
        from abjad.tools import scoretools
        candidate_shortest_leaf = self.leaves[0]
        for leaf in self.leaves[1:]:
            if (leaf._get_timespan().stop_offset <
                candidate_shortest_leaf._get_timespan().stop_offset):
                candidate_shortest_leaf = leaf
        next_leaf = candidate_shortest_leaf._get_in_my_logical_voice(
            1, prototype=scoretools.Leaf)
        next_vertical_moment = next_leaf._get_vertical_moment()
        return next_vertical_moment

    @property
    def notes(self):
        r'''Tuple of zero or more notes at vertical moment.
        '''
        from abjad.tools import scoretools
        result = []
        prototype = (scoretools.Note,)
        for component in self.components:
            if isinstance(component, prototype):
                result.append(component)
        result = tuple(result)
        return result

    @property
    def notes_and_chords(self):
        r'''Tuple of zero or more notes and chords at vertical moment.
        '''
        from abjad.tools import scoretools
        result = []
        prototype = (scoretools.Chord, scoretools.Note)
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
        from abjad.tools import scoretools
        result = [x for x in self.overlap_components
            if isinstance(x, scoretools.Leaf)]
        result = tuple(result)
        return result

    @property
    def overlap_measures(self):
        r'''Tuple of measures in vertical moment starting before vertical
        moment, ordered by score index.
        '''
        from abjad.tools import scoretools
        result = [x for x in self.overlap_components
            if isinstance(x, scoretools.Measure)]
        result = tuple(result)
        return result

    @property
    def overlap_notes(self):
        r'''Tuple of notes in vertical moment starting before vertical moment,
        ordered by score index.
        '''
        from abjad.tools import scoretools
        result = [x for x in self.overlap_components
            if isinstance(x, scoretools.Note)]
        result = tuple(result)
        return result

    @property
    def previous_vertical_moment(self):
        r'''Reference to previous vertical moment backward in time.
        '''
        from abjad.tools import scoretools
        if self.offset == 0:
            raise IndexError
        most_recent_start_offset = durationtools.Offset(0)
        token_leaf = None
        for leaf in self.leaves:
            #print ''
            #print leaf
            leaf_start = leaf._get_timespan().start_offset
            if leaf_start < self.offset:
                #print 'found leaf starting before this moment ...'
                if most_recent_start_offset <= leaf_start:
                    most_recent_start_offset = leaf_start
                    token_leaf = leaf
            else:
                #print 'found leaf starting on this moment ...'
                try:
                    previous_leaf = leaf._get_in_my_logical_voice(
                        -1, prototype=scoretools.Leaf)
                    start = previous_leaf._get_timespan().start_offset
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
        result = []
        for component in self.components:
            if component._get_timespan().start_offset == self.offset:
                result.append(component)
        result = tuple(result)
        return result

    @property
    def start_leaves(self):
        r'''Tuple of leaves in vertical moment starting with vertical moment,
        ordered by score index.
        '''
        from abjad.tools import scoretools
        result = [x for x in self.start_components
            if isinstance(x, scoretools.Leaf)]
        result = tuple(result)
        return result

    @property
    def start_notes(self):
        r'''Tuple of notes in vertical moment starting with vertical moment,
        ordered by score index.
        '''
        from abjad.tools import scoretools
        result = [x for x in self.start_components
            if isinstance(x, scoretools.Note)]
        result = tuple(result)
        return result
