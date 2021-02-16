from . import enumerate
from .iterate import Iteration
from .ordereddict import OrderedDict
from .parentage import Parentage
from .pitch.segments import PitchSegment
from .score import Chord, Leaf, Note
from .select import Selection
from .sequence import Sequence


class VerticalMoment:
    r'''
    Vertical moment.

    ..  container:: example

        >>> score = abjad.Score()
        >>> staff_group = abjad.StaffGroup()
        >>> staff_group.lilypond_type = 'PianoStaff'
        >>> staff_group.append(abjad.Staff("c'4 e'4 d'4 f'4"))
        >>> staff_group.append(abjad.Staff(r"""\clef "bass" g2 f2"""))
        >>> score.append(staff_group)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new PianoStaff
                <<
                    \new Staff
                    {
                        c'4
                        e'4
                        d'4
                        f'4
                    }
                    \new Staff
                    {
                        \clef "bass"
                        g2
                        f2
                    }
                >>
            >>

        >>> for moment in abjad.iterate_vertical_moments(score):
        ...     moment
        ...
        VerticalMoment(0, <<2>>)
        VerticalMoment(1/4, <<2>>)
        VerticalMoment(1/2, <<2>>)
        VerticalMoment(3/4, <<2>>)

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = "Selections"

    __slots__ = ("_components", "_governors", "_offset")

    ### INITIALIZER ###

    def __init__(self, components=None, offset=None):
        self._components = components
        self._offset = offset

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a vertical moment with the same
        components as this vertical moment.

        Returns true or false.
        """
        if isinstance(argument, VerticalMoment):
            if len(self) == len(argument):
                for c, d in zip(self.components, argument.components):
                    if c is not d:
                        return False
                else:
                    return True
        return False

    def __hash__(self):
        """
        Hases vertical moment.

        ..  container:: example

            Vertical moments can be hashed:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> vms = []
            >>> vms.extend(abjad.iterate_vertical_moments(staff))
            >>> vms.extend(abjad.iterate_vertical_moments(staff))

            >>> assert len(vms) == 8
            >>> assert len(set(vms)) == 4

        Redefined in tandem with __eq__.
        """
        if self.components:
            return hash(tuple([id(_) for _ in self.components]))
        return 0

    def __len__(self):
        r"""
        Length of vertical moment.

        ..  container:: example

            >>> score = abjad.Score(
            ... r'''
            ...    \new Staff {
            ...        \times 4/3 {
            ...            d''8
            ...            c''8
            ...            b'8
            ...        }
            ...    }
            ...    \new PianoStaff <<
            ...        \new Staff {
            ...            a'4
            ...            g'4
            ...        }
            ...        \new Staff {
            ...            \clef "bass"
            ...            f'8
            ...            e'8
            ...            d'8
            ...            c'8
            ...        }
            ...    >>
            ...    '''
            ...    )

            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \new Score
                <<
                    \new Staff
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 4/3 {
                            d''8
                            c''8
                            b'8
                        }
                    }
                    \new PianoStaff
                    <<
                        \new Staff
                        {
                            a'4
                            g'4
                        }
                        \new Staff
                        {
                            \clef "bass"
                            f'8
                            e'8
                            d'8
                            c'8
                        }
                    >>
                >>

            >>> for moment in abjad.iterate_vertical_moments(score):
            ...     print(moment, len(moment))
            ...
            VerticalMoment(0, <<3>>) 9
            VerticalMoment(1/8, <<3>>) 9
            VerticalMoment(1/6, <<3>>) 9
            VerticalMoment(1/4, <<3>>) 9
            VerticalMoment(1/3, <<3>>) 9
            VerticalMoment(3/8, <<3>>) 9

        Defined equal to the number of components in vertical moment.

        Returns nonnegative integer.
        """
        return len(self.components)

    def __repr__(self):
        """
        Gets interpreter representation of vertical moment.

        Returns string.
        """
        if not self.components:
            return f"{type(self).__name__}()"
        length = len(self.leaves)
        result = f"{type(self).__name__}({str(self.offset)}, <<{length}>>)"
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def attack_count(self):
        r"""
        Positive integer number of pitch carriers starting at vertical
        moment.

        ..  container:: example

            >>> score = abjad.Score(
            ... r'''
            ...    \new Staff {
            ...        \times 4/3 {
            ...            d''8
            ...            c''8
            ...            b'8
            ...        }
            ...    }
            ...    \new PianoStaff <<
            ...        \new Staff {
            ...            a'4
            ...            g'4
            ...        }
            ...        \new Staff {
            ...            \clef "bass"
            ...            f'8
            ...            e'8
            ...            d'8
            ...            c'8
            ...        }
            ...    >>
            ...    '''
            ...    )

            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \new Score
                <<
                    \new Staff
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 4/3 {
                            d''8
                            c''8
                            b'8
                        }
                    }
                    \new PianoStaff
                    <<
                        \new Staff
                        {
                            a'4
                            g'4
                        }
                        \new Staff
                        {
                            \clef "bass"
                            f'8
                            e'8
                            d'8
                            c'8
                        }
                    >>
                >>

            >>> for moment in abjad.iterate_vertical_moments(score):
            ...     print(moment, moment.attack_count)
            ...
            VerticalMoment(0, <<3>>) 3
            VerticalMoment(1/8, <<3>>) 1
            VerticalMoment(1/6, <<3>>) 1
            VerticalMoment(1/4, <<3>>) 2
            VerticalMoment(1/3, <<3>>) 1
            VerticalMoment(3/8, <<3>>) 1

        """
        leaves = []
        for leaf in self.start_leaves:
            if isinstance(leaf, (Note, Chord)):
                leaves.append(leaf)
        return len(leaves)

    @property
    def components(self):
        """
        Tuple of zero or more components happening at vertical moment.

        It is always the case that ``self.components =
        self.overlap_components + self.start_components``.
        """
        return self._components

    @property
    def governors(self):
        """
        Tuple of one or more containers in which vertical moment is evaluated.
        """
        return self._governors

    @property
    def leaves(self):
        r"""
        Tuple of zero or more leaves at vertical moment.

        ..  container:: example

            >>> score = abjad.Score(
            ... r'''
            ...    \new Staff {
            ...        \times 4/3 {
            ...            d''8
            ...            c''8
            ...            b'8
            ...        }
            ...    }
            ...    \new PianoStaff <<
            ...        \new Staff {
            ...            a'4
            ...            g'4
            ...        }
            ...        \new Staff {
            ...            \clef "bass"
            ...            f'8
            ...            e'8
            ...            d'8
            ...            c'8
            ...        }
            ...    >>
            ...    '''
            ...    )

            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \new Score
                <<
                    \new Staff
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 4/3 {
                            d''8
                            c''8
                            b'8
                        }
                    }
                    \new PianoStaff
                    <<
                        \new Staff
                        {
                            a'4
                            g'4
                        }
                        \new Staff
                        {
                            \clef "bass"
                            f'8
                            e'8
                            d'8
                            c'8
                        }
                    >>
                >>

            >>> for moment in abjad.iterate_vertical_moments(score):
            ...     print(moment.offset, moment.leaves)
            ...
            0 Selection([Note("d''8"), Note("a'4"), Note("f'8")])
            1/8 Selection([Note("d''8"), Note("a'4"), Note("e'8")])
            1/6 Selection([Note("c''8"), Note("a'4"), Note("e'8")])
            1/4 Selection([Note("c''8"), Note("g'4"), Note("d'8")])
            1/3 Selection([Note("b'8"), Note("g'4"), Note("d'8")])
            3/8 Selection([Note("b'8"), Note("g'4"), Note("c'8")])

        """
        result = []
        for component in self.components:
            if isinstance(component, Leaf):
                result.append(component)
        result = Selection(result)
        return result

    @property
    def notes(self):
        """
        Tuple of zero or more notes at vertical moment.
        """
        result = []
        for component in self.components:
            if isinstance(component, Note):
                result.append(component)
        result = tuple(result)
        return result

    @property
    def notes_and_chords(self):
        """
        Tuple of zero or more notes and chords at vertical moment.
        """
        result = []
        prototype = (Chord, Note)
        for component in self.components:
            if isinstance(component, prototype):
                result.append(component)
        result = tuple(result)
        return result

    @property
    def offset(self):
        """
        Rational-valued score offset at which vertical moment is evaluated.
        """
        return self._offset

    @property
    def overlap_components(self):
        """
        Tuple of components in vertical moment starting before vertical
        moment, ordered by score index.
        """
        result = []
        for component in self.components:
            if component.start < self.offset:
                result.append(component)
        result = tuple(result)
        return result

    @property
    def overlap_leaves(self):
        """
        Tuple of leaves in vertical moment starting before vertical moment,
        ordered by score index.
        """
        result = [x for x in self.overlap_components if isinstance(x, Leaf)]
        result = tuple(result)
        return result

    @property
    def overlap_notes(self):
        """
        Tuple of notes in vertical moment starting before vertical moment,
        ordered by score index.
        """
        result = self.overlap_components
        result = [_ for _ in result if isinstance(_, Note)]
        result = tuple(result)
        return result

    @property
    def start_components(self):
        """
        Tuple of components in vertical moment starting with at vertical
        moment, ordered by score index.
        """
        result = []
        for component in self.components:
            if component._get_timespan().start_offset == self.offset:
                result.append(component)
        result = tuple(result)
        return result

    @property
    def start_leaves(self):
        """
        Tuple of leaves in vertical moment starting with vertical moment,
        ordered by score index.
        """
        result = [x for x in self.start_components if isinstance(x, Leaf)]
        result = tuple(result)
        return result

    @property
    def start_notes(self):
        """
        Tuple of notes in vertical moment starting with vertical moment,
        ordered by score index.
        """
        result = [x for x in self.start_components if isinstance(x, Note)]
        result = tuple(result)
        return result


### FUNCTIONS ###


def iterate_vertical_moments(components, reverse=None):
    r'''
    Iterates vertical moments.

    ..  container:: example

        Iterates vertical moments:

        >>> score = abjad.Score([])
        >>> staff = abjad.Staff(r"\times 4/3 { d''8 c''8 b'8 }")
        >>> score.append(staff)
        >>> staff_group = abjad.StaffGroup([])
        >>> staff_group.lilypond_type = 'PianoStaff'
        >>> staff_group.append(abjad.Staff("a'4 g'4"))
        >>> staff_group.append(abjad.Staff(r"""\clef "bass" f'8 e'8 d'8 c'8"""))
        >>> score.append(staff_group)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 4/3 {
                        d''8
                        c''8
                        b'8
                    }
                }
                \new PianoStaff
                <<
                    \new Staff
                    {
                        a'4
                        g'4
                    }
                    \new Staff
                    {
                        \clef "bass"
                        f'8
                        e'8
                        d'8
                        c'8
                    }
                >>
            >>

        >>> for vertical_moment in abjad.iterate_vertical_moments(score):
        ...     vertical_moment.leaves
        ...
        Selection([Note("d''8"), Note("a'4"), Note("f'8")])
        Selection([Note("d''8"), Note("a'4"), Note("e'8")])
        Selection([Note("c''8"), Note("a'4"), Note("e'8")])
        Selection([Note("c''8"), Note("g'4"), Note("d'8")])
        Selection([Note("b'8"), Note("g'4"), Note("d'8")])
        Selection([Note("b'8"), Note("g'4"), Note("c'8")])

        >>> for vertical_moment in abjad.iterate_vertical_moments(staff_group):
        ...     vertical_moment.leaves
        ...
        Selection([Note("a'4"), Note("f'8")])
        Selection([Note("a'4"), Note("e'8")])
        Selection([Note("g'4"), Note("d'8")])
        Selection([Note("g'4"), Note("c'8")])

    ..  container:: example

        Iterates vertical moments in reverse:

        >>> score = abjad.Score([])
        >>> staff = abjad.Staff(r"\times 4/3 { d''8 c''8 b'8 }")
        >>> score.append(staff)
        >>> staff_group = abjad.StaffGroup([])
        >>> staff_group.lilypond_type = 'PianoStaff'
        >>> staff_group.append(abjad.Staff("a'4 g'4"))
        >>> staff_group.append(abjad.Staff(r"""\clef "bass" f'8 e'8 d'8 c'8"""))
        >>> score.append(staff_group)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 4/3 {
                        d''8
                        c''8
                        b'8
                    }
                }
                \new PianoStaff
                <<
                    \new Staff
                    {
                        a'4
                        g'4
                    }
                    \new Staff
                    {
                        \clef "bass"
                        f'8
                        e'8
                        d'8
                        c'8
                    }
                >>
            >>

        >>> for vertical_moment in abjad.iterate_vertical_moments(score, reverse=True):
        ...     vertical_moment.leaves
        ...
        Selection([Note("b'8"), Note("g'4"), Note("c'8")])
        Selection([Note("b'8"), Note("g'4"), Note("d'8")])
        Selection([Note("c''8"), Note("g'4"), Note("d'8")])
        Selection([Note("c''8"), Note("a'4"), Note("e'8")])
        Selection([Note("d''8"), Note("a'4"), Note("e'8")])
        Selection([Note("d''8"), Note("a'4"), Note("f'8")])

        >>> for vertical_moment in abjad.iterate_vertical_moments(
        ...     staff_group,
        ...     reverse=True,
        ...     ):
        ...     vertical_moment.leaves
        ...
        Selection([Note("g'4"), Note("c'8")])
        Selection([Note("g'4"), Note("d'8")])
        Selection([Note("a'4"), Note("e'8")])
        Selection([Note("a'4"), Note("f'8")])

    Returns tuple.
    '''
    moments = []
    components = list(Selection(components).components())
    components.sort(key=lambda _: _._get_timespan().start_offset)
    offset_to_components = OrderedDict()
    for component in components:
        start_offset = component._get_timespan().start_offset
        if start_offset not in offset_to_components:
            offset_to_components[start_offset] = []
    # TODO: optimize with bisect
    for component in components:
        inserted = False
        timespan = component._get_timespan()
        for offset, list_ in offset_to_components.items():
            if (
                timespan.start_offset <= offset < timespan.stop_offset
                and component not in list_
            ):
                list_.append(component)
                inserted = True
            elif inserted is True:
                break
    moments = []
    for offset, list_ in offset_to_components.items():
        list_.sort(key=lambda _: Parentage(_).score_index())
        moment = VerticalMoment(components=list_, offset=offset)
        moments.append(moment)
    if reverse is True:
        moments.reverse()
    return tuple(moments)


def iterate_leaf_pairs(components):
    r"""
    Iterates leaf pairs.

    ..  container:: example

        >>> score = abjad.Score()
        >>> score.append(abjad.Staff("c'8 d'8 e'8 f'8 g'4"))
        >>> score.append(abjad.Staff("c4 a,4 g,4"))
        >>> abjad.attach(abjad.Clef('bass'), score[1][0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    c'8
                    d'8
                    e'8
                    f'8
                    g'4
                }
                \new Staff
                {
                    \clef "bass"
                    c4
                    a,4
                    g,4
                }
            >>

        >>> for leaf_pair in abjad.iterate_leaf_pairs(score):
        ...     leaf_pair
        Selection([Note("c'8"), Note('c4')])
        Selection([Note("c'8"), Note("d'8")])
        Selection([Note('c4'), Note("d'8")])
        Selection([Note("d'8"), Note("e'8")])
        Selection([Note("d'8"), Note('a,4')])
        Selection([Note('c4'), Note("e'8")])
        Selection([Note('c4'), Note('a,4')])
        Selection([Note("e'8"), Note('a,4')])
        Selection([Note("e'8"), Note("f'8")])
        Selection([Note('a,4'), Note("f'8")])
        Selection([Note("f'8"), Note("g'4")])
        Selection([Note("f'8"), Note('g,4')])
        Selection([Note('a,4'), Note("g'4")])
        Selection([Note('a,4'), Note('g,4')])
        Selection([Note("g'4"), Note('g,4')])

    Iterates leaf pairs left-to-right and top-to-bottom.

    Returns generator.
    """
    vertical_moments = iterate_vertical_moments(components)
    for moment_1, moment_2 in Sequence(vertical_moments).nwise():
        for pair in enumerate.yield_pairs(moment_1.start_leaves):
            yield Selection(pair)
        sequences = [moment_1.leaves, moment_2.start_leaves]
        for pair in enumerate.yield_outer_product(sequences):
            yield Selection(pair)
    else:
        for pair in enumerate.yield_pairs(moment_2.start_leaves):
            yield Selection(pair)


def iterate_pitch_pairs(components):
    r"""
    Iterates pitch pairs.

    ..  container:: example

        Iterates note pitch pairs:

        >>> score = abjad.Score()
        >>> score.append(abjad.Staff("c'8 d' e' f' g'4"))
        >>> score.append(abjad.Staff("c4 a, g,"))
        >>> abjad.attach(abjad.Clef('bass'), score[1][0])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    c'8
                    d'8
                    e'8
                    f'8
                    g'4
                }
                \new Staff
                {
                    \clef "bass"
                    c4
                    a,4
                    g,4
                }
            >>

        >>> for pair in abjad.iterate_pitch_pairs(score):
        ...     pair
        PitchSegment("c' c")
        PitchSegment("c' d'")
        PitchSegment("c d'")
        PitchSegment("d' e'")
        PitchSegment("d' a,")
        PitchSegment("c e'")
        PitchSegment("c a,")
        PitchSegment("e' a,")
        PitchSegment("e' f'")
        PitchSegment("a, f'")
        PitchSegment("f' g'")
        PitchSegment("f' g,")
        PitchSegment("a, g'")
        PitchSegment("a, g,")
        PitchSegment("g' g,")

    ..  container:: example

        Iterates chord pitch pairs:

        >>> staff = abjad.Staff("<c' d' e'>4 <f'' g''>4")

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                <c' d' e'>4
                <f'' g''>4
            }

        >>> for pair in abjad.iterate_pitch_pairs(staff):
        ...     pair
        ...
        PitchSegment("c' d'")
        PitchSegment("c' e'")
        PitchSegment("d' e'")
        PitchSegment("c' f''")
        PitchSegment("c' g''")
        PitchSegment("d' f''")
        PitchSegment("d' g''")
        PitchSegment("e' f''")
        PitchSegment("e' g''")
        PitchSegment("f'' g''")

    Returns generator.
    """
    for leaf_pair in iterate_leaf_pairs(components):
        pitches = sorted(Iteration(leaf_pair[0]).pitches())
        for pair in enumerate.yield_pairs(pitches):
            yield PitchSegment(pair)
        if isinstance(leaf_pair, set):
            pitches = sorted(Iteration(leaf_pair).pitches())
            for pair in enumerate.yield_pairs(pitches):
                yield PitchSegment(pair)
        else:
            pitches_1 = sorted(Iteration(leaf_pair[0]).pitches())
            pitches_2 = sorted(Iteration(leaf_pair[1]).pitches())
            sequences = [pitches_1, pitches_2]
            for pair in enumerate.yield_outer_product(sequences):
                yield PitchSegment(pair)
        pitches = sorted(Iteration(leaf_pair[1]).pitches())
        for pair in enumerate.yield_pairs(pitches):
            yield PitchSegment(pair)
