from abjad.tools import quantizationtools
import copy


def test_QGridContainer___copy___01():

    tree = quantizationtools.QGridContainer(
        preprolated_duration=1,
        children=[
            quantizationtools.QGridLeaf(preprolated_duration=1),
            quantizationtools.QGridContainer(
                preprolated_duration=2,
                children=[
                    quantizationtools.QGridLeaf(preprolated_duration=3),
                    quantizationtools.QGridContainer(
                        preprolated_duration=4,
                        children=[
                            quantizationtools.QGridLeaf(preprolated_duration=1),
                            quantizationtools.QGridLeaf(preprolated_duration=1),
                            quantizationtools.QGridLeaf(preprolated_duration=1)
                        ])
                ]),
            quantizationtools.QGridLeaf(preprolated_duration=2)
        ])

    copied = copy.copy(tree)

    assert tree == copied
    assert tree is not copied

    assert tree[0] == copied[0]
    assert tree[0] is not copied[0]

    assert tree[1] == copied[1]
    assert tree[1] is not copied[1]

    assert tree[2] == copied[2]
    assert tree[2] is not copied[2]

