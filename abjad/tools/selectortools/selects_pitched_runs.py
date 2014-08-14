# -*- encoding: utf-8 -*-


def selects_pitched_runs():
    r'''Selects first logical tie in pitched runs.

    ..  container:: example

        ::

            >>> selector = selectortools.selects_pitched_runs()
            >>> print(format(selector))
            selectortools.Selector(
                callbacks=(
                    selectortools.PrototypeSelectorCallback(
                        scoretools.Leaf
                        ),
                    selectortools.RunSelectorCallback(
                        (
                            scoretools.Note,
                            scoretools.Chord,
                            )
                        ),
                    ),
                )

        ::

            >>> staff = Staff()
            >>> staff.extend(r"c'4. d'8 ~ \times 2/3 { d'4 r4 e'4 ~ } e'8 f'4.")
            >>> print(format(staff))
            \new Staff {
                c'4.
                d'8 ~
                \times 2/3 {
                    d'4
                    r4
                    e'4 ~
                }
                e'8
                f'4.
            }

        ::

            >>> for x in selector(staff):
            ...     x
            ...
            Selection(Note("c'4."), Note("d'8"), Note("d'4"))
            Selection(Note("e'4"), Note("e'8"), Note("f'4."))

    '''
    from abjad.tools import scoretools
    from experimental.tools import selectortools
    selector = selectortools.Selector()
    selector = selector.by_leaves()
    selector = selector.by_run((scoretools.Note, scoretools.Chord))
    return selector