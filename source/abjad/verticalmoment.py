"""
Classes to model events that happen at the same time.
"""

import typing

from . import enumerate as _enumerate
from . import iterate as _iterate
from . import parentage as _parentage
from . import pitch as _pitch
from . import score as _score
from . import select as _select
from . import sequence as _sequence


class VerticalMoment:
    r'''
    Vertical moment.

    ..  container:: example

        >>> score = abjad.Score()
        >>> staff_group = abjad.StaffGroup()
        >>> staff_group.set_lilypond_type('PianoStaff')
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

    __slots__ = ("_components", "_governors", "_offset")

    ### INITIALIZER ###

    def __init__(self, components=None, offset=None):
        self._components = components or ()
        self._offset = offset

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        if isinstance(argument, type(self)):
            if len(self) == len(argument):
                for c, d in zip(self.get_components(), argument.get_components()):
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
        if self.get_components():
            return hash(tuple([id(_) for _ in self.get_components()]))
        return 0

    def __len__(self) -> int:
        r"""
        Gets length of vertical moment.

        ..  container:: example

            >>> score = abjad.Score([
            ...     abjad.Staff(r"\tuplet 3/2 { d''4 c''4 b'4 }"),
            ...     abjad.StaffGroup([
            ...         abjad.Staff("a'4 g'4"),
            ...         abjad.Staff(r'''\clef "bass" f'8 e'8 d'8 c'8'''),
            ...     ]),
            ... ])
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \new Score
                <<
                    \new Staff
                    {
                        \tuplet 3/2
                        {
                            d''4
                            c''4
                            b'4
                        }
                    }
                    \new StaffGroup
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
        return len(self.get_components())

    def __repr__(self) -> str:
        """
        Gets interpreter representation of vertical moment.
        """
        if not self.get_components():
            return f"{type(self).__name__}()"
        length = len(self.get_leaves())
        result = f"{type(self).__name__}({str(self.get_offset())}, <<{length}>>)"
        return result

    ### PUBLIC PROPERTIES ###

    def get_attack_count(self) -> int:
        r"""
        Positive integer number of pitch carriers starting at vertical moment.

        ..  container:: example

            >>> score = abjad.Score([
            ...     abjad.Staff(r"\tuplet 3/2 { d''4 c''4 b'4 }"),
            ...     abjad.StaffGroup([
            ...         abjad.Staff("a'4 g'4"),
            ...         abjad.Staff(r'''\clef "bass" f'8 e'8 d'8 c'8'''),
            ...     ]),
            ... ])
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \new Score
                <<
                    \new Staff
                    {
                        \tuplet 3/2
                        {
                            d''4
                            c''4
                            b'4
                        }
                    }
                    \new StaffGroup
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
            ...     print(moment, moment.get_attack_count())
            ...
            VerticalMoment(0, <<3>>) 3
            VerticalMoment(1/8, <<3>>) 1
            VerticalMoment(1/6, <<3>>) 1
            VerticalMoment(1/4, <<3>>) 2
            VerticalMoment(1/3, <<3>>) 1
            VerticalMoment(3/8, <<3>>) 1

        """
        leaves = []
        for leaf in self.get_start_leaves():
            if isinstance(leaf, _score.Note | _score.Chord):
                leaves.append(leaf)
        return len(leaves)

    def get_components(self):
        """
        Tuple of zero or more components happening at vertical moment.

        It is always the case that ``self.get_components() ==
        self.get_overlap_components() + self.get_start_components()``.
        """
        return self._components

    def get_governors(self):
        """
        Tuple of one or more containers in which vertical moment is evaluated.
        """
        return self._governors

    def get_leaves(self) -> list[_score.Leaf]:
        r"""
        Tuple of zero or more leaves at vertical moment.

        ..  container:: example

            >>> score = abjad.Score([
            ...     abjad.Staff(r"\tuplet 3/2 { d''4 c''4 b'4 }"),
            ...     abjad.StaffGroup([
            ...         abjad.Staff("a'4 g'4"),
            ...         abjad.Staff(r'''\clef "bass" f'8 e'8 d'8 c'8'''),
            ...     ]),
            ... ])
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \new Score
                <<
                    \new Staff
                    {
                        \tuplet 3/2
                        {
                            d''4
                            c''4
                            b'4
                        }
                    }
                    \new StaffGroup
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
            ...     print(moment.get_offset(), moment.get_leaves())
            ...
            0 [Note("d''4"), Note("a'4"), Note("f'8")]
            1/8 [Note("d''4"), Note("a'4"), Note("e'8")]
            1/6 [Note("c''4"), Note("a'4"), Note("e'8")]
            1/4 [Note("c''4"), Note("g'4"), Note("d'8")]
            1/3 [Note("b'4"), Note("g'4"), Note("d'8")]
            3/8 [Note("b'4"), Note("g'4"), Note("c'8")]

        """
        result = []
        for component in self.get_components():
            if isinstance(component, _score.Leaf):
                result.append(component)
        return result

    def get_notes(self):
        """
        Tuple of zero or more notes at vertical moment.
        """
        result = []
        for component in self.get_components():
            if isinstance(component, _score.Note):
                result.append(component)
        result = tuple(result)
        return result

    def get_notes_and_chords(self):
        """
        Tuple of zero or more notes and chords at vertical moment.
        """
        result = []
        prototype = (_score.Chord, _score.Note)
        for component in self.get_components():
            if isinstance(component, prototype):
                result.append(component)
        result = tuple(result)
        return result

    def get_offset(self):
        """
        Rational-valued score offset at which vertical moment is evaluated.
        """
        return self._offset

    def get_overlap_components(self):
        """
        Tuple of components in vertical moment starting before vertical
        moment, ordered by score index.
        """
        result = []
        for component in self.get_components():
            if component.start < self.get_offset():
                result.append(component)
        result = tuple(result)
        return result

    def get_overlap_leaves(self):
        """
        Tuple of leaves in vertical moment starting before vertical moment,
        ordered by score index.
        """
        result = [x for x in self.overlap_components if isinstance(x, _score.Leaf)]
        result = tuple(result)
        return result

    def get_overlap_notes(self):
        """
        Tuple of notes in vertical moment starting before vertical moment,
        ordered by score index.
        """
        result = self.overlap_components
        result = [_ for _ in result if isinstance(_, _score.Note)]
        result = tuple(result)
        return result

    def get_start_components(self):
        """
        Tuple of components in vertical moment starting with at vertical
        moment, ordered by score index.
        """
        result = []
        for component in self.get_components():
            if component._get_timespan().start_offset == self.get_offset():
                result.append(component)
        result = tuple(result)
        return result

    def get_start_leaves(self):
        """
        Tuple of leaves in vertical moment starting with vertical moment,
        ordered by score index.
        """
        result = [x for x in self.get_start_components() if isinstance(x, _score.Leaf)]
        result = tuple(result)
        return result

    def get_start_notes(self):
        """
        Tuple of notes in vertical moment starting with vertical moment,
        ordered by score index.
        """
        result = [x for x in self.get_start_components() if isinstance(x, _score.Note)]
        result = tuple(result)
        return result


### FUNCTIONS ###


def iterate_vertical_moments(components, *, reverse=False):
    r"""
    Iterates vertical moments.

    Returns tuple.

    ..  container:: example

        Iterates vertical moments forward:

        >>> score = abjad.Score([
        ...     abjad.Staff(r"\tuplet 3/2 { d''4 c''4 b'4 }"),
        ...     abjad.StaffGroup([
        ...         abjad.Staff("a'4 g'4"),
        ...         abjad.Staff(r'''\clef "bass" f'8 e'8 d'8 c'8'''),
        ...     ]),
        ... ])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tuplet 3/2
                    {
                        d''4
                        c''4
                        b'4
                    }
                }
                \new StaffGroup
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
        ...     vertical_moment.get_leaves()
        ...
        [Note("d''4"), Note("a'4"), Note("f'8")]
        [Note("d''4"), Note("a'4"), Note("e'8")]
        [Note("c''4"), Note("a'4"), Note("e'8")]
        [Note("c''4"), Note("g'4"), Note("d'8")]
        [Note("b'4"), Note("g'4"), Note("d'8")]
        [Note("b'4"), Note("g'4"), Note("c'8")]

        >>> staff_group = score[1]
        >>> for vertical_moment in abjad.iterate_vertical_moments(staff_group):
        ...     vertical_moment.get_leaves()
        ...
        [Note("a'4"), Note("f'8")]
        [Note("a'4"), Note("e'8")]
        [Note("g'4"), Note("d'8")]
        [Note("g'4"), Note("c'8")]

    ..  container:: example

        Iterates vertical moments in reverse:

        >>> for vmoment in abjad.iterate_vertical_moments(score, reverse=True):
        ...     vmoment.get_leaves()
        ...
        [Note("b'4"), Note("g'4"), Note("c'8")]
        [Note("b'4"), Note("g'4"), Note("d'8")]
        [Note("c''4"), Note("g'4"), Note("d'8")]
        [Note("c''4"), Note("a'4"), Note("e'8")]
        [Note("d''4"), Note("a'4"), Note("e'8")]
        [Note("d''4"), Note("a'4"), Note("f'8")]

        >>> for vmoment in abjad.iterate_vertical_moments(staff_group, reverse=True):
        ...     vmoment.get_leaves()
        ...
        [Note("g'4"), Note("c'8")]
        [Note("g'4"), Note("d'8")]
        [Note("a'4"), Note("e'8")]
        [Note("a'4"), Note("f'8")]

    """
    moments = []
    components = _select.components(components)
    components.sort(key=lambda _: _._get_timespan().start_offset)
    offset_to_components = dict()
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
        list_.sort(key=lambda _: _parentage.Parentage(_).score_index())
        moment = VerticalMoment(components=list_, offset=offset)
        moments.append(moment)
    if reverse is True:
        moments.reverse()
    return tuple(moments)


def iterate_leaf_pairs(components) -> typing.Iterator:
    r"""
    Iterates leaf pairs.

    Iterates leaf pairs left-to-right and top-to-bottom.

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
        [Note("c'8"), Note('c4')]
        [Note("c'8"), Note("d'8")]
        [Note('c4'), Note("d'8")]
        [Note("d'8"), Note("e'8")]
        [Note("d'8"), Note('a,4')]
        [Note('c4'), Note("e'8")]
        [Note('c4'), Note('a,4')]
        [Note("e'8"), Note('a,4')]
        [Note("e'8"), Note("f'8")]
        [Note('a,4'), Note("f'8")]
        [Note("f'8"), Note("g'4")]
        [Note("f'8"), Note('g,4')]
        [Note('a,4'), Note("g'4")]
        [Note('a,4'), Note('g,4')]
        [Note("g'4"), Note('g,4')]

    """
    vertical_moments = iterate_vertical_moments(components)
    for moment_1, moment_2 in _sequence.nwise(vertical_moments):
        for pair in _enumerate.yield_pairs(moment_1.get_start_leaves()):
            yield list(pair)
        sequences = [moment_1.get_leaves(), moment_2.get_start_leaves()]
        for pair in _enumerate.outer_product(sequences):
            yield list(pair)
    else:
        for pair in _enumerate.yield_pairs(moment_2.get_start_leaves()):
            yield list(pair)


def iterate_pitch_pairs(
    components,
) -> typing.Iterator[tuple[_pitch.NamedPitch, _pitch.NamedPitch]]:
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
        (NamedPitch("c'"), NamedPitch('c'))
        (NamedPitch("c'"), NamedPitch("d'"))
        (NamedPitch('c'), NamedPitch("d'"))
        (NamedPitch("d'"), NamedPitch("e'"))
        (NamedPitch("d'"), NamedPitch('a,'))
        (NamedPitch('c'), NamedPitch("e'"))
        (NamedPitch('c'), NamedPitch('a,'))
        (NamedPitch("e'"), NamedPitch('a,'))
        (NamedPitch("e'"), NamedPitch("f'"))
        (NamedPitch('a,'), NamedPitch("f'"))
        (NamedPitch("f'"), NamedPitch("g'"))
        (NamedPitch("f'"), NamedPitch('g,'))
        (NamedPitch('a,'), NamedPitch("g'"))
        (NamedPitch('a,'), NamedPitch('g,'))
        (NamedPitch("g'"), NamedPitch('g,'))

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
        (NamedPitch("c'"), NamedPitch("d'"))
        (NamedPitch("c'"), NamedPitch("e'"))
        (NamedPitch("d'"), NamedPitch("e'"))
        (NamedPitch("c'"), NamedPitch("f''"))
        (NamedPitch("c'"), NamedPitch("g''"))
        (NamedPitch("d'"), NamedPitch("f''"))
        (NamedPitch("d'"), NamedPitch("g''"))
        (NamedPitch("e'"), NamedPitch("f''"))
        (NamedPitch("e'"), NamedPitch("g''"))
        (NamedPitch("f''"), NamedPitch("g''"))

    """
    for leaf_pair in iterate_leaf_pairs(components):
        pitches = sorted(_iterate.pitches(leaf_pair[0]))
        for pair in _enumerate.yield_pairs(pitches):
            yield tuple(pair)
        if isinstance(leaf_pair, set):
            pitches = sorted(_iterate.pitches(leaf_pair))
            for pair in _enumerate.yield_pairs(pitches):
                yield tuple(pair)
        else:
            pitches_1 = sorted(_iterate.pitches(leaf_pair[0]))
            pitches_2 = sorted(_iterate.pitches(leaf_pair[1]))
            sequences = [pitches_1, pitches_2]
            for pair in _enumerate.outer_product(sequences):
                yield tuple(pair)
        pitches = sorted(_iterate.pitches(leaf_pair[1]))
        for pair in _enumerate.yield_pairs(pitches):
            yield tuple(pair)
