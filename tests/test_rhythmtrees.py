import copy
import pickle

import pytest

import abjad


def test_RhythmTreeContainer___call___01():
    rtm = "(1 (1 (2 (1 1 1)) 2))"
    rtc = abjad.rhythmtrees.RhythmTreeParser()(rtm)[0]
    result = rtc(abjad.Duration(1, 4))
    assert isinstance(result, list)
    assert len(result) == 1
    assert abjad.lilypond(result[0]) == abjad.string.normalize(
        r"""
        \tuplet 5/4
        {
            c'16
            \tuplet 3/2
            {
                c'16
                c'16
                c'16
            }
            c'8
        }
        """
    )


def test_RhythmTreeContainer___call___02():
    rtm = "(1 (1 (2 (1 1 1 1)) 1))"
    rtc = abjad.rhythmtrees.RhythmTreeParser()(rtm)[0]
    components = rtc(abjad.Duration(1, 4))
    # tuplet = components[0]._parent
    # staff = abjad.Staff([tuplet])
    staff = abjad.Staff(components)
    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 1/1
            {
                c'16
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 1/1
                {
                    c'32
                    c'32
                    c'32
                    c'32
                }
                c'16
            }
        }
        """
    ), print(staff)


def test_RhythmTreeContainer___contains___01():
    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf((1, 1))
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf((1, 1))
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf((1, 1))
    subcontainer = abjad.rhythmtrees.RhythmTreeContainer((1, 1), children=[leaf_b])
    container = abjad.rhythmtrees.RhythmTreeContainer(
        (1, 1), children=[leaf_a, subcontainer]
    )
    assert leaf_a in container
    assert leaf_b not in container
    assert leaf_c not in container


def test_RhythmTreeContainer___eq___01():
    a = abjad.rhythmtrees.RhythmTreeContainer((1, 1))
    b = abjad.rhythmtrees.RhythmTreeContainer((1, 1))
    assert repr(a) == repr(b)
    assert a != b


def test_RhythmTreeContainer___eq___02():
    a = abjad.rhythmtrees.RhythmTreeContainer(
        (1, 1), children=[abjad.rhythmtrees.RhythmTreeLeaf((1, 1))]
    )
    b = abjad.rhythmtrees.RhythmTreeContainer(
        (1, 1), children=[abjad.rhythmtrees.RhythmTreeLeaf((1, 1))]
    )
    assert repr(a) == repr(b)
    assert a != b


def test_RhythmTreeContainer___eq___03():
    a = abjad.rhythmtrees.RhythmTreeContainer((1, 1))
    b = abjad.rhythmtrees.RhythmTreeContainer((2, 1), children=[])
    c = abjad.rhythmtrees.RhythmTreeContainer(
        (1, 1),
        children=[abjad.rhythmtrees.RhythmTreeLeaf((1, 1))],
    )
    d = abjad.rhythmtrees.RhythmTreeContainer(
        (2, 1),
        children=[abjad.rhythmtrees.RhythmTreeLeaf((1, 1))],
    )
    e = abjad.rhythmtrees.RhythmTreeContainer(
        (2, 1),
        children=[abjad.rhythmtrees.RhythmTreeLeaf((2, 1))],
    )
    assert a != b
    assert a != c
    assert a != d
    assert a != e
    assert b != c
    assert b != d
    assert b != e
    assert c != d
    assert c != e
    assert d != e


def test_RhythmTreeContainer___getitem___01():
    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf((2, 1))
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf((1, 1))
    container = abjad.rhythmtrees.RhythmTreeContainer(
        (1, 1), children=[leaf_a, leaf_b, leaf_c]
    )
    assert container[0] is leaf_a
    assert container[1] is leaf_b
    assert container[2] is leaf_c
    with pytest.raises(Exception):
        container[3]
    assert container[-1] is leaf_c
    assert container[-2] is leaf_b
    assert container[-3] is leaf_a
    with pytest.raises(Exception):
        container[-4]


def test_RhythmTreeContainer___init___01():
    container = abjad.rhythmtrees.RhythmTreeContainer((1, 1))
    assert container.children == ()
    assert container.pair == (1, 1)
    assert container.start_offset == 0
    assert container.parent is None


def test_RhythmTreeContainer___init___02():
    container = abjad.rhythmtrees.RhythmTreeContainer((2, 1), children=[])
    assert container.children == ()
    assert container.pair == (2, 1)
    assert container.start_offset == 0
    assert container.parent is None


def test_RhythmTreeContainer___init___03():
    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf((1, 1))
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf((2, 1))
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf((1, 1))
    assert leaf_a.start_offset == 0
    assert leaf_a.parent is None
    assert leaf_b.start_offset == 0
    assert leaf_b.parent is None
    assert leaf_c.start_offset == 0
    assert leaf_c.parent is None
    container = abjad.rhythmtrees.RhythmTreeContainer(
        (4, 1), children=[leaf_a, leaf_b, leaf_c]
    )
    assert container.children == (leaf_a, leaf_b, leaf_c)
    assert container.pair == (4, 1)
    assert container.start_offset == 0
    assert container.parent is None
    assert leaf_a.start_offset == 0
    assert leaf_a.parent is container
    assert leaf_b.start_offset == 1
    assert leaf_b.parent is container
    assert leaf_c.start_offset == 3
    assert leaf_c.parent is container


def test_RhythmTreeContainer___iter___01():
    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf((2, 1))
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf((1, 1))
    container = abjad.rhythmtrees.RhythmTreeContainer(
        (1, 1), children=[leaf_a, leaf_b, leaf_c]
    )
    assert [_ for _ in container] == [leaf_a, leaf_b, leaf_c]


def test_RhythmTreeContainer___len___01():
    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf((2, 1))
    subcontainer = abjad.rhythmtrees.RhythmTreeContainer(
        (2, 1), children=[leaf_b, leaf_c]
    )
    leaf_d = abjad.rhythmtrees.RhythmTreeLeaf((1, 1))
    container = abjad.rhythmtrees.RhythmTreeContainer(
        (1, 1), children=[leaf_a, subcontainer, leaf_d]
    )
    assert len(container) == 3


def test_RhythmTreeContainer_append_01():
    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf((2, 1))
    leaf_d = abjad.rhythmtrees.RhythmTreeLeaf((1, 1))
    container = abjad.rhythmtrees.RhythmTreeContainer((1, 1))
    assert container.children == ()
    container.append(leaf_a)
    assert container.children == (leaf_a,)
    container.append(leaf_b)
    assert container.children == (leaf_a, leaf_b)
    container.append(leaf_c)
    assert container.children == (leaf_a, leaf_b, leaf_c)
    container.append(leaf_d)
    assert container.children == (leaf_a, leaf_b, leaf_c, leaf_d)
    container.append(leaf_a)
    assert container.children == (leaf_b, leaf_c, leaf_d, leaf_a)


def test_RhythmTreeContainer_children_01():
    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf((2, 1))
    subcontainer = abjad.rhythmtrees.RhythmTreeContainer(
        (2, 1), children=[leaf_b, leaf_c]
    )
    leaf_d = abjad.rhythmtrees.RhythmTreeLeaf((1, 1))
    container = abjad.rhythmtrees.RhythmTreeContainer(
        (1, 1), children=[leaf_a, subcontainer, leaf_d]
    )
    assert container.children == (leaf_a, subcontainer, leaf_d)


def test_RhythmTreeContainer_contents_duration_01():
    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf((2, 1))
    subcontainer = abjad.rhythmtrees.RhythmTreeContainer(
        (2, 1), children=[leaf_b, leaf_c]
    )
    leaf_d = abjad.rhythmtrees.RhythmTreeLeaf((1, 1))
    container = abjad.rhythmtrees.RhythmTreeContainer(
        (1, 1), children=[leaf_a, subcontainer, leaf_d]
    )
    assert container._get_contents_duration() == 6
    assert subcontainer._get_contents_duration() == 5


def test_RhythmTreeContainer_extend_01():
    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf((2, 1))
    leaf_d = abjad.rhythmtrees.RhythmTreeLeaf((1, 1))
    container = abjad.rhythmtrees.RhythmTreeContainer((1, 1))
    assert container.children == ()
    container.extend([leaf_a])
    assert container.children == (leaf_a,)
    container.extend([leaf_b, leaf_c, leaf_d])
    assert container.children == (leaf_a, leaf_b, leaf_c, leaf_d)
    container.extend([leaf_a, leaf_c])
    assert container.children == (leaf_b, leaf_d, leaf_a, leaf_c)


def test_RhythmTreeContainer_index_01():
    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf((2, 1))
    subcontainer = abjad.rhythmtrees.RhythmTreeContainer(
        (2, 1), children=[leaf_b, leaf_c]
    )
    leaf_d = abjad.rhythmtrees.RhythmTreeLeaf((1, 1))
    container = abjad.rhythmtrees.RhythmTreeContainer(
        (1, 1), children=[leaf_a, subcontainer, leaf_d]
    )
    assert container.index(leaf_a) == 0
    assert container.index(subcontainer) == 1
    assert container.index(leaf_d) == 2
    with pytest.raises(ValueError):
        container.index(leaf_b)
    with pytest.raises(ValueError):
        container.index(leaf_c)


def test_RhythmTreeContainer_insert_01():
    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf((2, 1))
    container = abjad.rhythmtrees.RhythmTreeContainer((1, 1))
    assert container.children == ()
    container.insert(0, leaf_a)
    assert container.children == (leaf_a,)
    container.insert(0, leaf_b)
    assert container.children == (leaf_b, leaf_a)
    container.insert(1, leaf_c)
    assert container.children == (leaf_b, leaf_c, leaf_a)


def test_RhythmTreeContainer_pop_01():
    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf((2, 1))
    container = abjad.rhythmtrees.RhythmTreeContainer(
        (1, 1), children=[leaf_a, leaf_b, leaf_c]
    )
    assert container.children == (leaf_a, leaf_b, leaf_c)
    assert leaf_a.parent is container
    assert leaf_b.parent is container
    assert leaf_c.parent is container
    result = container.pop()
    assert container.children == (leaf_a, leaf_b)
    assert result is leaf_c
    assert result.parent is None
    result = container.pop(0)
    assert container.children == (leaf_b,)
    assert result is leaf_a
    assert result.parent is None


def test_RhythmTreeContainer_remove_01():
    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf((2, 1))
    container = abjad.rhythmtrees.RhythmTreeContainer(
        (1, 1), children=[leaf_a, leaf_b, leaf_c]
    )
    assert container.children == (leaf_a, leaf_b, leaf_c)
    assert leaf_a.parent is container
    assert leaf_b.parent is container
    assert leaf_c.parent is container
    container.remove(leaf_a)
    assert container.children == (leaf_b, leaf_c)
    assert leaf_a.parent is None
    container.remove(leaf_c)
    assert container.children == (leaf_b,)
    assert leaf_c.parent is None


def test_RhythmTreeContainer_rtm_format_01():
    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf((3, 1))
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf((2, 1))
    subcontainer = abjad.rhythmtrees.RhythmTreeContainer(
        (2, 1), children=[leaf_b, leaf_c]
    )
    leaf_d = abjad.rhythmtrees.RhythmTreeLeaf((1, 1))
    container = abjad.rhythmtrees.RhythmTreeContainer(
        (1, 1),
        children=[leaf_a, subcontainer, leaf_d],
    )
    assert subcontainer.rtm_format == "(2 (3 2))"
    assert container.rtm_format == "(1 (3 (2 (3 2)) 1))"


def test_RhythmTreeLeaf___copy___01():
    rtl = abjad.rhythmtrees.RhythmTreeLeaf((1, 1))
    copied = copy.copy(rtl)
    assert repr(rtl) == repr(copied)
    assert rtl is not copied


def test_RhythmTreeLeaf___copy___02():
    rtl = abjad.rhythmtrees.RhythmTreeLeaf((2, 1), is_pitched=True)
    copied = copy.copy(rtl)
    assert repr(rtl) == repr(copied)
    assert rtl is not copied


def test_RhythmTreeLeaf___eq___01():
    a = abjad.rhythmtrees.RhythmTreeLeaf((1, 1), is_pitched=True)
    b = abjad.rhythmtrees.RhythmTreeLeaf((1, 1), is_pitched=True)
    assert repr(a) == repr(b)
    assert a != b


def test_RhythmTreeLeaf___eq___02():
    a = abjad.rhythmtrees.RhythmTreeLeaf((1, 1), is_pitched=True)
    b = abjad.rhythmtrees.RhythmTreeLeaf((1, 1), is_pitched=False)
    c = abjad.rhythmtrees.RhythmTreeLeaf((2, 1), is_pitched=True)
    d = abjad.rhythmtrees.RhythmTreeLeaf((2, 1), is_pitched=False)
    assert a != b
    assert a != c
    assert a != d
    assert b != c
    assert b != d
    assert c != d


def test_RhythmTreeNode___call___01():
    rtm = "(1 (1 1 1 1))"
    rtc = abjad.rhythmtrees.RhythmTreeParser()(rtm)[0]
    components = rtc(abjad.Duration(1, 4))
    assert len(components) == 1
    tuplet = components[0]
    assert len(tuplet) == 4
    assert all(isinstance(_, abjad.Note) for _ in tuplet)
    assert all(_.written_duration == abjad.Duration(1, 16) for _ in tuplet)


def test_RhythmTreeNode___call___02():
    rtm = "(1 (1 (2 (1 1 1)) 2))"
    rtc = abjad.rhythmtrees.RhythmTreeParser()(rtm)[0]
    result = rtc(abjad.Duration(1, 4))
    assert isinstance(result, list)
    assert len(result) == 1
    assert abjad.lilypond(result[0]) == abjad.string.normalize(
        r"""
        \tuplet 5/4
        {
            c'16
            \tuplet 3/2
            {
                c'16
                c'16
                c'16
            }
            c'8
        }
        """
    )


def test_RhythmTreeNode___call___03():
    rtm = "(1 (1 (2 (1 (2 (1 1)) 1)) 2))"
    rtc = abjad.rhythmtrees.RhythmTreeParser()(rtm)[0]
    components = rtc(abjad.Duration(1, 4))
    staff = abjad.Staff(components)
    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \tuplet 5/4
            {
                c'16
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 1/1
                {
                    c'32
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 1/1
                    {
                        c'32
                        c'32
                    }
                    c'32
                }
                c'8
            }
        }
        """
    )


def test_RhythmTreeNode_depth_01():
    container = abjad.rhythmtrees.RhythmTreeContainer((1, 1))
    assert container.depth == 0
    rtl = abjad.rhythmtrees.RhythmTreeLeaf((1, 1))
    assert rtl.depth == 0
    container.append(rtl)
    assert rtl.depth == 1
    subcontainer = abjad.rhythmtrees.RhythmTreeContainer((1, 1))
    assert subcontainer.depth == 0
    container.append(subcontainer)
    assert subcontainer.depth == 1
    subcontainer.append(rtl)
    assert rtl.depth == 2
    subsubcontainer = abjad.rhythmtrees.RhythmTreeContainer((1, 1))
    assert subsubcontainer.depth == 0
    subcontainer.append(subsubcontainer)
    assert subsubcontainer.depth == 2
    subsubcontainer.append(rtl)
    assert rtl.depth == 3


def test_RhythmTreeNode_duration_01():
    rtc = abjad.rhythmtrees.RhythmTreeContainer(
        (1, 1),
        children=[
            abjad.rhythmtrees.RhythmTreeLeaf((1, 1)),
            abjad.rhythmtrees.RhythmTreeContainer(
                (2, 1),
                children=[
                    abjad.rhythmtrees.RhythmTreeLeaf((3, 1)),
                    abjad.rhythmtrees.RhythmTreeLeaf((2, 1)),
                ],
            ),
            abjad.rhythmtrees.RhythmTreeLeaf((2, 1)),
        ],
    )
    assert rtc.duration == abjad.Duration(1, 1)
    assert rtc[0].duration == abjad.Duration(1, 5)
    assert rtc[1].duration == abjad.Duration(2, 5)
    assert rtc[1][0].duration == abjad.Duration(6, 25)
    assert rtc[1][1].duration == abjad.Duration(4, 25)
    assert rtc[2].duration == abjad.Duration(2, 5)
    rtc[1].append(rtc.pop())
    assert rtc.duration == abjad.Duration(1, 1)
    assert rtc[0].duration == abjad.Duration(1, 3)
    assert rtc[1].duration == abjad.Duration(2, 3)
    assert rtc[1][0].duration == abjad.Duration(6, 21)
    assert rtc[1][1].duration == abjad.Duration(4, 21)
    assert rtc[1][2].duration == abjad.Duration(4, 21)
    rtc.pair = (19, 1)
    assert rtc.duration == abjad.Duration(19, 1)
    assert rtc[0].duration == abjad.Duration(19, 3)
    assert rtc[1].duration == abjad.Duration(38, 3)
    assert rtc[1][0].duration == abjad.Duration(114, 21)
    assert rtc[1][1].duration == abjad.Duration(76, 21)
    assert rtc[1][2].duration == abjad.Duration(76, 21)


def test_RhythmTreeNode_offset_01():
    rtc = abjad.rhythmtrees.RhythmTreeContainer(
        (1, 1),
        children=[
            abjad.rhythmtrees.RhythmTreeLeaf((1, 1)),
            abjad.rhythmtrees.RhythmTreeContainer(
                (2, 1),
                children=[
                    abjad.rhythmtrees.RhythmTreeLeaf((3, 1)),
                    abjad.rhythmtrees.RhythmTreeLeaf((2, 1)),
                ],
            ),
            abjad.rhythmtrees.RhythmTreeLeaf((2, 1)),
        ],
    )
    assert rtc.start_offset == abjad.Offset(0)
    assert rtc[0].start_offset == abjad.Offset(0)
    assert rtc[1].start_offset == abjad.Offset(1, 5)
    assert rtc[1][0].start_offset == abjad.Offset(1, 5)
    assert rtc[1][1].start_offset == abjad.Offset(11, 25)
    assert rtc[2].start_offset == abjad.Offset(3, 5)
    node = rtc.pop()
    assert node.start_offset == abjad.Offset(0)
    rtc[1].append(node)
    assert rtc.start_offset == abjad.Offset(0)
    assert rtc[0].start_offset == abjad.Offset(0)
    assert rtc[1].start_offset == abjad.Offset(1, 3)
    assert rtc[1][0].start_offset == abjad.Offset(1, 3)
    assert rtc[1][1].start_offset == abjad.Offset(13, 21)
    assert rtc[1][2].start_offset == abjad.Offset(17, 21)
    rtc.pair = (19, 1)
    assert rtc.start_offset == abjad.Offset(0)
    assert rtc[0].start_offset == abjad.Offset(0)
    assert rtc[1].start_offset == abjad.Offset(19, 3)
    assert rtc[1][0].start_offset == abjad.Offset(19, 3)
    assert rtc[1][1].start_offset == abjad.Offset(247, 21)
    assert rtc[1][2].start_offset == abjad.Offset(323, 21)


def test_RhythmTreeNode_parent_01():
    rtl = abjad.rhythmtrees.RhythmTreeLeaf((1, 1))
    container = abjad.rhythmtrees.RhythmTreeContainer((1, 1))
    subcontainer = abjad.rhythmtrees.RhythmTreeContainer((1, 1))
    assert rtl.parent is None
    assert container.parent is None
    assert subcontainer.parent is None
    container.append(rtl)
    assert rtl.parent is container
    container.append(subcontainer)
    assert subcontainer.parent is container
    assert rtl.parent is container
    assert container.parent is None
    subcontainer.append(rtl)
    assert rtl.parent is subcontainer
    assert subcontainer.parent is container
    assert container.parent is None
    with pytest.raises(ValueError):
        subcontainer.append(container)


def test_RhythmTreeNode__get_parentage_ratios_01():
    string = "(1 (1 (2 (3 4)) 2))"
    rtc = abjad.rhythmtrees.RhythmTreeParser()(string)[0]
    assert rtc._get_parentage_ratios() == ((1, 1),)
    assert rtc[0]._get_parentage_ratios() == ((1, 1), (1, 5))
    assert rtc[1]._get_parentage_ratios() == ((1, 1), (2, 5))
    assert rtc[1][0]._get_parentage_ratios() == ((1, 1), (2, 5), (3, 7))
    assert rtc[1][1]._get_parentage_ratios() == ((1, 1), (2, 5), (4, 7))
    assert rtc[2]._get_parentage_ratios() == ((1, 1), (2, 5))


def test_RhythmTreeNode_pickle_01():
    string = "(1 (1 (2 (1 1 1)) 2))"
    rtc = abjad.rhythmtrees.RhythmTreeParser()(string)[0]
    pickled = pickle.loads(pickle.dumps(rtc))
    assert repr(pickled) == repr(rtc)
    assert pickled != rtc
    assert pickled is not rtc


def test_RhythmTreeNode_root_01():
    rtl = abjad.rhythmtrees.RhythmTreeLeaf((1, 1))
    subsubcontainer = abjad.rhythmtrees.RhythmTreeContainer((1, 1))
    subcontainer = abjad.rhythmtrees.RhythmTreeContainer((1, 1))
    container = abjad.rhythmtrees.RhythmTreeContainer((1, 1))
    container.append(subcontainer)
    subcontainer.append(subsubcontainer)
    subsubcontainer.append(rtl)
    assert rtl.root is container
    assert subsubcontainer.root is container
    assert subcontainer.root is container
    assert container.root is None
