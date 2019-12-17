from abjad.top.inspect import inspect


class VerticalMoment(object):
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

            >>> abjad.f(score)
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

        >>> for moment in abjad.iterate(score).vertical_moments():
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
            >>> vms.extend(abjad.iterate(staff).vertical_moments())
            >>> vms.extend(abjad.iterate(staff).vertical_moments())

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

                >>> abjad.f(score)
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

            >>> for moment in abjad.iterate(score).vertical_moments():
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

                >>> abjad.f(score)
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

            >>> for moment in abjad.iterate(score).vertical_moments():
            ...     print(moment, moment.attack_count)
            ...
            VerticalMoment(0, <<3>>) 3
            VerticalMoment(1/8, <<3>>) 1
            VerticalMoment(1/6, <<3>>) 1
            VerticalMoment(1/4, <<3>>) 2
            VerticalMoment(1/3, <<3>>) 1
            VerticalMoment(3/8, <<3>>) 1

        """
        from .Chord import Chord
        from .Note import Note

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

                >>> abjad.f(score)
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

            >>> for moment in abjad.iterate(score).vertical_moments():
            ...     print(moment.offset, moment.leaves)
            ...
            0 Selection([Note("d''8"), Note("a'4"), Note("f'8")])
            1/8 Selection([Note("d''8"), Note("a'4"), Note("e'8")])
            1/6 Selection([Note("c''8"), Note("a'4"), Note("e'8")])
            1/4 Selection([Note("c''8"), Note("g'4"), Note("d'8")])
            1/3 Selection([Note("b'8"), Note("g'4"), Note("d'8")])
            3/8 Selection([Note("b'8"), Note("g'4"), Note("c'8")])

        """
        from .Leaf import Leaf
        from .Selection import Selection

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
        from .Note import Note

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
        from .Chord import Chord
        from .Note import Note

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
        from .Leaf import Leaf

        result = [x for x in self.overlap_components if isinstance(x, Leaf)]
        result = tuple(result)
        return result

    @property
    def overlap_notes(self):
        """
        Tuple of notes in vertical moment starting before vertical moment,
        ordered by score index.
        """
        from .Note import Note

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
            if inspect(component).timespan().start_offset == self.offset:
                result.append(component)
        result = tuple(result)
        return result

    @property
    def start_leaves(self):
        """
        Tuple of leaves in vertical moment starting with vertical moment,
        ordered by score index.
        """
        from .Leaf import Leaf

        result = [x for x in self.start_components if isinstance(x, Leaf)]
        result = tuple(result)
        return result

    @property
    def start_notes(self):
        """
        Tuple of notes in vertical moment starting with vertical moment,
        ordered by score index.
        """
        from .Note import Note

        result = [x for x in self.start_components if isinstance(x, Note)]
        result = tuple(result)
        return result
