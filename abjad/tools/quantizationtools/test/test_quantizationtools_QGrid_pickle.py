# -*- coding: utf-8 -*-
import pickle
from abjad import *


def test_quantizationtools_QGrid_pickle_01():
    q_grid = quantizationtools.QGrid(
        root_node=quantizationtools.QGridContainer(
            preprolated_duration=1,
            children=[
                quantizationtools.QGridLeaf(
                    preprolated_duration=1,
                    q_event_proxies=[
                        quantizationtools.QEventProxy(
                            quantizationtools.SilentQEvent(100),
                            0.5,
                            ),
                        ],
                    ),
                ],
            ),
        next_downbeat=quantizationtools.QGridLeaf(
            preprolated_duration=1,
            q_event_proxies=[
                quantizationtools.QEventProxy(
                    quantizationtools.TerminalQEvent(200),
                    0.9,
                    ),
                ],
            ),
        )
    pickled = pickle.loads(pickle.dumps(q_grid))

    assert format(pickled) == format(q_grid)
    assert pickled is not q_grid
    assert pickled != q_grid, \
        systemtools.TestManager.diff(pickled, q_grid, 'Diff:')
