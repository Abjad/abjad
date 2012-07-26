from experimental import quantizationtools
import copy


def test_QGridContainer___copy___01():

    tree = quantizationtools.QGridContainer(1, [
        quantizationtools.QGridLeaf(1),
        quantizationtools.QGridContainer(2, [
            quantizationtools.QGridLeaf(3),
            quantizationtools.QGridContainer(4, [
                quantizationtools.QGridLeaf(1),
                quantizationtools.QGridLeaf(1),
                quantizationtools.QGridLeaf(1)
                ])
            ]),
        quantizationtools.QGridLeaf(2)
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

