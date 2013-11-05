# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import sequencetools
import py.test


def test_datastructuretools_CyclicList___getitem___01():

    cyclic_list = datastructuretools.CyclicList(range(3))
    assert cyclic_list[0] == 0
    assert cyclic_list[1] == 1
    assert cyclic_list[2] == 2
    assert cyclic_list[3] == 0
    assert cyclic_list[4] == 1
    assert cyclic_list[5] == 2


def test_datastructuretools_CyclicList___getitem___02():

    cyclic_list = datastructuretools.CyclicList(range(3))
    assert cyclic_list[-0] == 0
    assert cyclic_list[-1] == 2
    assert cyclic_list[-2] == 1
    assert cyclic_list[-3] == 0
    assert cyclic_list[-4] == 2
    assert cyclic_list[-5] == 1


def test_datastructuretools_CyclicList___getitem___03():

    cyclic_list = datastructuretools.CyclicList([])
    assert py.test.raises(IndexError, 'cyclic_list[0]')
    assert py.test.raises(IndexError, 'cyclic_list[1]')
    assert py.test.raises(IndexError, 'cyclic_list[-1]')
