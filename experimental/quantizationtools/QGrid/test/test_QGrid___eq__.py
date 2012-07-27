from experimental import quantizationtools


def test_QGrid___eq___01():

    a = quantizationtools.QGrid()
    b = quantizationtools.QGrid()

    assert a == b


def test_QGrid___eq___02():

    a = quantizationtools.QGrid(
        root_node=quantizationtools.QGridContainer(1, [
            quantizationtools.QGridLeaf(1, q_events=[
                quantizationtools.QEventProxy(
                    quantizationtools.SilentQEvent(100),
                    0.5
                    )
                ])
            ]),
        next_downbeat=quantizationtools.QGridLeaf(1,
            q_events=[
                quantizationtools.QEventProxy(
                    quantizationtools.TerminalQEvent(200),
                    0.9
                    )
                ]
            )
        )

    b = quantizationtools.QGrid( 
        root_node=quantizationtools.QGridContainer(1, [  
            quantizationtools.QGridLeaf(1, q_events=[ 
                quantizationtools.QEventProxy( 
                    quantizationtools.SilentQEvent(100),
                    0.5
                    )
                ])
            ]),
        next_downbeat=quantizationtools.QGridLeaf(1, 
            q_events=[ 
                quantizationtools.QEventProxy( 
                    quantizationtools.TerminalQEvent(200),
                    0.9
                    )
                ]
            )
        )

    a == b


def test_QGrid___eq___03():

    a = quantizationtools.QGrid()
    b = quantizationtools.QGrid(
        root_node=quantizationtools.QGridContainer(1, [
            quantizationtools.QGridLeaf(1, q_events=[
                quantizationtools.QEventProxy(
                    quantizationtools.SilentQEvent(100),
                    0.5
                    )
                ])
            ])
        )
    c = quantizationtools.QGrid(
        next_downbeat=quantizationtools.QGridLeaf(1,
            q_events=[ 
                quantizationtools.QEventProxy(
                    quantizationtools.TerminalQEvent(200),
                    0.9
                    )
                ]
            )
        )
    d = quantizationtools.QGrid(
        root_node=quantizationtools.QGridContainer(1, [
            quantizationtools.QGridLeaf(1, q_events=[
                quantizationtools.QEventProxy(
                    quantizationtools.SilentQEvent(100),
                    0.5
                    )
                ])
            ]),
        next_downbeat=quantizationtools.QGridLeaf(1,
            q_events=[
                quantizationtools.QEventProxy(
                    quantizationtools.TerminalQEvent(200),
                    0.9
                    )
                ]
            )
        )

    assert a != b
    assert a != c
    assert a != d

    assert b != c
    assert b != d

    assert c != d
