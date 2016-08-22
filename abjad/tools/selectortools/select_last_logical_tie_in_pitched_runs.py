# -*- coding: utf-8 -*-


def select_last_logical_tie_in_pitched_runs(expr=None):
    r'''Selects last logical tie in pitched runs.

    ..  container:: example

        ::

            >>> selector = selectortools.select_last_logical_tie_in_pitched_runs()
            >>> print(format(selector))
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
                    selectortools.ItemSelectorCallback(
                        item=-1,
                        apply_to_each=True,
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
            LogicalTie([Note("d'8"), Note("d'4")])
            LogicalTie([Note("f'4.")])

    '''
    from abjad.tools import selectortools
    selector = selectortools.select_pitched_runs()
    selector = selector.by_logical_tie(flatten=False)
    selector = selector[-1]
    if expr is None:
        return selector
    return selector(expr)
