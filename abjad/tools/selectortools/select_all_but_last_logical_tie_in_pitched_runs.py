# -*- coding: utf-8 -*-


def select_all_but_last_logical_tie_in_pitched_runs(expr=None):
    r'''Selects all but last logical tie in pitched runs.

    ..  container:: example

        ::

            >>> selector = selectortools.select_all_but_last_logical_tie_in_pitched_runs()
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
                    selectortools.SliceSelectorCallback(
                        stop=-1,
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
            >>> print(format(staff))
            \new Staff {
                c'4
                d'4 ~
                \times 2/3 {
                    d'4
                    e'4
                    r4
                }
                f'4
                g'4
                \times 2/3 {
                    r4
                    a'4
                    b'4 ~
                }
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
    from abjad.tools import selectortools
    selector = selectortools.select_pitched_runs()
    selector = selector.by_logical_tie(flatten=False)
    selector = selector[:-1]
    selector = selector.flatten(depth=1)
    if expr is None:
        return selector
    return selector(expr)
