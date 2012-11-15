from experimental import quantizationtools
import pickle


def test_QGrid_pickle_01():

    q_grid = quantizationtools.QGrid(
        root_node=quantizationtools.QGridContainer(1, [
            quantizationtools.QGridLeaf(1, q_event_proxies=[
                quantizationtools.QEventProxy(
                    quantizationtools.SilentQEvent(100),
                    0.5
                    )
                ])
            ]),
        next_downbeat=quantizationtools.QGridLeaf(1,
            q_event_proxies=[
                quantizationtools.QEventProxy(
                    quantizationtools.TerminalQEvent(200),
                    0.9
                    )
                ]
            )
        )

    pickled = pickle.loads(pickle.dumps(q_grid))

    assert pickled == q_grid
    assert pickled is not q_grid
    
