# -*- encoding: utf-8 -*-


def selects_first_logical_tie_in_pitched_runs():
    r'''Selects first logical tie in pitched runs.

    ..  container:: example

        >>> selector = selectortools.selects_first_logical_tie_in_pitched_runs()
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
                selectortools.LogicalTieSelectorCallback(
                    flatten=False,
                    pitched=False,
                    trivial=True,
                    only_with_head=False,
                    only_with_tail=False,
                    ),
                selectortools.SliceSelectorCallback(
                    argument=0,
                    apply_to_each=True,
                    ),
                ),
            )

    '''
    from experimental.tools import selectortools
    selector = selectortools.selects_pitched_runs()
    selector = selector.by_logical_tie(flatten=False)
    selector = selector[0]
    return selector