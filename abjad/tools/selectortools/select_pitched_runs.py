# -*- coding: utf-8 -*-


def select_pitched_runs(argument=None):
    r'''Selects pitched runs.

    ..  container:: example

        ::

            >>> selector = selectortools.select_pitched_runs()
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
                    ),
                )

        ::

            >>> staff = Staff()
            >>> staff.extend(r"c'4. d'8 ~ \times 2/3 { d'4 r4 e'4 ~ } e'8 f'4.")
            >>> result = selector(staff)
            >>> label(result).color_alternating()
            >>> set_(staff).auto_beaming = False
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

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
    from abjad.tools import scoretools
    from abjad.tools import selectortools
    selector = selectortools.Selector()
    selector = selector.by_leaf()
    selector = selector.by_run((scoretools.Note, scoretools.Chord))
    if argument is None:
        return selector
    return selector(argument)
