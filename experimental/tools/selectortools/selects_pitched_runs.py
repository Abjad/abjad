# -*- encoding: utf-8 -*-


def selects_pitched_runs():
    r'''Selects first logical tie in pitched runs.

    ..  container:: example

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

    '''

    from abjad.tools import scoretools
    from experimental.tools import selectortools
    selector = selectortools.Selector()
    selector = selector.by_leaves()
    selector = selector.by_run((scoretools.Note, scoretools.Chord))
    return selector