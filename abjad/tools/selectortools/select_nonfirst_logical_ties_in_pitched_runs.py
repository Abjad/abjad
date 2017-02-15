# -*- coding: utf-8 -*-


def select_nonfirst_logical_ties_in_pitched_runs(argument=None):
    r'''Selects nonfirst logical ties in pitched runs.

    ..  container:: example

        ::

            >>> selector = selectortools.select_nonfirst_logical_ties_in_pitched_runs()
            >>> f(selector)
            selectortools.Selector(
                callbacks=(
                    selectortools.PrototypeSelectorCallback(
                        prototype=scoretools.Leaf,
                        ),
                    selectortools.RunSelectorCallback(
                        prototype=(
                            scoretools.Note,
                            scoretools.Chord,
                            ),
                        ),
                    selectortools.LogicalTieSelectorCallback(
                        flatten=False,
                        pitched=False,
                        trivial=True,
                        ),
                    selectortools.SliceSelectorCallback(
                        start=1,
                        apply_to_each=True,
                        ),
                    selectortools.FlattenSelectorCallback(
                        depth=1,
                        ),
                    ),
                )

        ::

            >>> staff = Staff("c' d' ~ d' e' r f' g' r a' b' ~ b' c''")
            >>> tuplet = Tuplet((2, 3), staff[2:5])
            >>> tuplet = Tuplet((2, 3), staff[5:8])
            >>> result = selector(staff)
            >>> label(result).color_alternating()
            >>> set_(staff).auto_beaming = False
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

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
    from abjad.tools import selectortools
    selector = selectortools.select_pitched_runs()
    selector = selector.by_logical_tie(flatten=False)
    selector = selector[1:]
    selector = selector.flatten(depth=1)
    if argument is None:
        return selector
    return selector(argument)
