# -*- coding: utf-8 -*-


class SelectorLibrary(object):
    r'''Selector library.

    ::

        >>> import abjad

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Selectors'

    @staticmethod
    def select_first_logical_tie_in_pitched_runs(argument=None):
        r'''Selects first logical tie in pitched runs.

        ..  container:: example

            ::

                >>> library = abjad.SelectorLibrary
                >>> selector = library.select_first_logical_tie_in_pitched_runs()
                >>> f(selector)
                abjad.Selector(
                    callbacks=(
                        abjad.PrototypeSelectorCallback(
                            prototype=abjad.Leaf,
                            ),
                        abjad.RunSelectorCallback(
                            prototype=(
                                abjad.Note,
                                abjad.Chord,
                                ),
                            ),
                        abjad.LogicalTieSelectorCallback(
                            flatten=False,
                            pitched=False,
                            trivial=True,
                            ),
                        abjad.ItemSelectorCallback(
                            item=0,
                            apply_to_each=True,
                            ),
                        ),
                    )

            ::

                >>> string = r"c'4. d'8 ~ \times 2/3 { d'4 r4 e'4 ~ } e'8 f'4."
                >>> staff = abjad.Staff(string)
                >>> result = selector(staff)
                >>> abjad.label(result).color_alternating()
                >>> abjad.setting(staff).auto_beaming = False
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        autoBeaming = ##f
                    } {
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        c'4.
                        d'8 ~
                        \times 2/3 {
                            d'4
                            r4
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            e'4 ~
                        }
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        e'8
                        f'4.
                    }

            ::

                >>> for item in result:
                ...     item
                ...
                LogicalTie([Note("c'4.")])
                LogicalTie([Note("e'4"), Note("e'8")])

        '''
        selector = SelectorLibrary.select_pitched_runs()
        selector = selector.by_logical_tie(flatten=False)
        selector = selector[0]
        if argument is None:
            return selector
        return selector(argument)

    @staticmethod
    def select_last_logical_tie_in_pitched_runs(argument=None):
        r'''Selects last logical tie in pitched runs.

        ..  container:: example

            ::

                >>> library = abjad.SelectorLibrary
                >>> selector = library.select_last_logical_tie_in_pitched_runs()
                >>> f(selector)
                abjad.Selector(
                    callbacks=(
                        abjad.PrototypeSelectorCallback(
                            prototype=abjad.Leaf,
                            ),
                        abjad.RunSelectorCallback(
                            prototype=(
                                abjad.Note,
                                abjad.Chord,
                                ),
                            ),
                        abjad.LogicalTieSelectorCallback(
                            flatten=False,
                            pitched=False,
                            trivial=True,
                            ),
                        abjad.ItemSelectorCallback(
                            item=-1,
                            apply_to_each=True,
                            ),
                        ),
                    )

            ::

                >>> string = r"c'4. d'8 ~ \times 2/3 { d'4 r4 e'4 ~ } e'8 f'4."
                >>> staff = abjad.Staff(string)
                >>> result = selector(staff)
                >>> abjad.label(result).color_alternating()
                >>> abjad.setting(staff).auto_beaming = False
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    c'4.
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'8 ~
                    \times 2/3 {
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'4
                        r4
                        e'4 ~
                    }
                    e'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    f'4.
                }

            ::

                >>> for item in result:
                ...     item
                ...
                LogicalTie([Note("d'8"), Note("d'4")])
                LogicalTie([Note("f'4.")])

        '''
        selector = SelectorLibrary.select_pitched_runs()
        selector = selector.by_logical_tie(flatten=False)
        selector = selector[-1]
        if argument is None:
            return selector
        return selector(argument)

    @staticmethod
    def select_nonfirst_logical_ties_in_pitched_runs(argument=None):
        r'''Selects nonfirst logical ties in pitched runs.

        ..  container:: example

            ::

                >>> library = abjad.SelectorLibrary
                >>> selector = library.select_nonfirst_logical_ties_in_pitched_runs()
                >>> f(selector)
                abjad.Selector(
                    callbacks=(
                        abjad.PrototypeSelectorCallback(
                            prototype=abjad.Leaf,
                            ),
                        abjad.RunSelectorCallback(
                            prototype=(
                                abjad.Note,
                                abjad.Chord,
                                ),
                            ),
                        abjad.LogicalTieSelectorCallback(
                            flatten=False,
                            pitched=False,
                            trivial=True,
                            ),
                        abjad.SliceSelectorCallback(
                            start=1,
                            apply_to_each=True,
                            ),
                        abjad.FlattenSelectorCallback(
                            depth=1,
                            ),
                        ),
                    )

            ::

                >>> staff = abjad.Staff(
                ...     r"c' d' ~ \times 2/3 { d' e' r } "
                ...     r"f' g' \times 2/3 { r a' b' ~ } b' c''"
                ...     )
                >>> result = selector(staff)
                >>> abjad.label(result).color_alternating()
                >>> abjad.setting(staff).auto_beaming = False
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff \with {
                    autoBeaming = ##f
                } {
                    c'4
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    d'4 ~
                    \times 2/3 {
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'4
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        e'4
                        r4
                    }
                    f'4
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    g'4
                    \times 2/3 {
                        r4
                        a'4
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        b'4 ~
                    }
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    b'4
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c''4
                }

            ::

                >>> for item in result:
                ...     item
                ...
                LogicalTie([Note("d'4"), Note("d'4")])
                LogicalTie([Note("e'4")])
                LogicalTie([Note("g'4")])
                LogicalTie([Note("b'4"), Note("b'4")])
                LogicalTie([Note("c''4")])

        '''
        selector = SelectorLibrary.select_pitched_runs()
        selector = selector.by_logical_tie(flatten=False)
        selector = selector[1:]
        selector = selector.flatten(depth=1)
        if argument is None:
            return selector
        return selector(argument)

    @staticmethod
    def select_nonlast_logical_ties_in_pitched_runs(argument=None):
        r'''Selects nonlast logical ties in pitched runs.

        ..  container:: example

            ::

                >>> library = abjad.SelectorLibrary
                >>> selector = library.select_nonlast_logical_ties_in_pitched_runs()
                >>> f(selector)
                abjad.Selector(
                    callbacks=(
                        abjad.PrototypeSelectorCallback(
                            prototype=abjad.Leaf,
                            ),
                        abjad.RunSelectorCallback(
                            prototype=(
                                abjad.Note,
                                abjad.Chord,
                                ),
                            ),
                        abjad.LogicalTieSelectorCallback(
                            flatten=False,
                            pitched=False,
                            trivial=True,
                            ),
                        abjad.SliceSelectorCallback(
                            stop=-1,
                            apply_to_each=True,
                            ),
                        abjad.FlattenSelectorCallback(
                            depth=1,
                            ),
                        ),
                    )

            ::

                >>> staff = abjad.Staff(
                ...     r"c' d' ~ \times 2/3 { d' e' r } "
                ...     r"f' g' \times 2/3 { r a' b' ~ } b' c''"
                ...     )
                >>> result = selector(staff)
                >>> abjad.label(result).color_alternating()
                >>> abjad.setting(staff).auto_beaming = False
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        autoBeaming = ##f
                    } {
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        c'4
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        d'4 ~
                        \times 2/3 {
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            d'4
                            e'4
                            r4
                        }
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        f'4
                        g'4
                        \times 2/3 {
                            r4
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            a'4
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            b'4 ~
                        }
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        b'4
                        c''4
                    }

            ::

                >>> for x in selector(staff):
                ...     x
                ...
                LogicalTie([Note("c'4")])
                LogicalTie([Note("d'4"), Note("d'4")])
                LogicalTie([Note("f'4")])
                LogicalTie([Note("a'4")])
                LogicalTie([Note("b'4"), Note("b'4")])

        '''
        selector = SelectorLibrary.select_pitched_runs()
        selector = selector.by_logical_tie(flatten=False)
        selector = selector[:-1]
        selector = selector.flatten(depth=1)
        if argument is None:
            return selector
        return selector(argument)

    @staticmethod
    def select_pitched_runs(argument=None):
        r'''Selects pitched runs.

        ..  container:: example

            ::

                >>> selector = abjad.SelectorLibrary.select_pitched_runs()
                >>> f(selector)
                abjad.Selector(
                    callbacks=(
                        abjad.PrototypeSelectorCallback(
                            prototype=abjad.Leaf,
                            ),
                        abjad.RunSelectorCallback(
                            prototype=(
                                abjad.Note,
                                abjad.Chord,
                                ),
                            ),
                        ),
                    )

            ::

                >>> string = r"c'4. d'8 ~ \times 2/3 { d'4 r4 e'4 ~ } e'8 f'4."
                >>> staff = abjad.Staff(string)
                >>> result = selector(staff)
                >>> abjad.label(result).color_alternating()
                >>> abjad.setting(staff).auto_beaming = False
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                    >>> f(staff)
                    \new Staff \with {
                        autoBeaming = ##f
                    } {
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        c'4.
                        \once \override Accidental.color = #red
                        \once \override Beam.color = #red
                        \once \override Dots.color = #red
                        \once \override NoteHead.color = #red
                        \once \override Stem.color = #red
                        d'8 ~
                        \times 2/3 {
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            d'4
                            r4
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            e'4 ~
                        }
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        e'8
                        \once \override Accidental.color = #blue
                        \once \override Beam.color = #blue
                        \once \override Dots.color = #blue
                        \once \override NoteHead.color = #blue
                        \once \override Stem.color = #blue
                        f'4.
                    }

            ::

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'4."), Note("d'8"), Note("d'4")])
                Selection([Note("e'4"), Note("e'8"), Note("f'4.")])

        '''
        import abjad
        selector = abjad.Selector()
        selector = selector.by_leaf()
        selector = selector.by_run((abjad.Note, abjad.Chord))
        if argument is None:
            return selector
        return selector(argument)
