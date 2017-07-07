# -*- coding: utf-8 -*-


def select_last_logical_tie_in_pitched_runs(argument=None):
    r'''Selects last logical tie in pitched runs.

    ..  container:: example

        ::

            >>> selector = selectortools.select_last_logical_tie_in_pitched_runs()
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

            >>> staff = Staff()
            >>> staff.extend(r"c'4. d'8 ~ \times 2/3 { d'4 r4 e'4 ~ } e'8 f'4.")
            >>> result = selector(staff)
            >>> label(result).color_alternating()
            >>> setting(staff).auto_beaming = False
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
    from abjad.tools import selectortools
    selector = selectortools.select_pitched_runs()
    selector = selector.by_logical_tie(flatten=False)
    selector = selector[-1]
    if argument is None:
        return selector
    return selector(argument)
