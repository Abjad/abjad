# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Component__logical_measure_number_01():

    staff = Staff("c'4 d' e' f' g' a' b' c''")
    attach(TimeSignature((2, 4)), staff[0])
    attach(TimeSignature((3, 4)), staff[4])
    attach(TimeSignature((1, 4)), staff[7])
    staff._update_logical_measure_numbers()

    assert staff._logical_measure_number == 1
    assert staff[0]._logical_measure_number == 1
    assert staff[1]._logical_measure_number == 1
    assert staff[2]._logical_measure_number == 2
    assert staff[3]._logical_measure_number == 2
    assert staff[4]._logical_measure_number == 3
    assert staff[5]._logical_measure_number == 3
    assert staff[6]._logical_measure_number == 3
    assert staff[7]._logical_measure_number == 4


def test_scoretools_Component__logical_measure_number_02():

    
    staff = Staff()
    staff.append(Measure((2, 4), "c'4 d'4"))
    staff.append(Measure((2, 4), "e'4 f'4"))
    staff.append(Measure((3, 4), "g'4 a'4 b'4"))
    staff.append(Measure((1, 4), "c''4"))
    staff._update_logical_measure_numbers()

    assert staff._logical_measure_number == 1

    assert staff[0]._logical_measure_number == 1
    assert staff[1]._logical_measure_number == 2
    assert staff[2]._logical_measure_number == 3
    assert staff[3]._logical_measure_number == 4

    leaves = iterate(staff).by_class(scoretools.Leaf)
    leaves = list(leaves)
    assert leaves[0]._logical_measure_number == 1
    assert leaves[1]._logical_measure_number == 1
    assert leaves[2]._logical_measure_number == 2
    assert leaves[3]._logical_measure_number == 2
    assert leaves[4]._logical_measure_number == 3
    assert leaves[5]._logical_measure_number == 3
    assert leaves[6]._logical_measure_number == 3
    assert leaves[7]._logical_measure_number == 4


def test_scoretools_Component__logical_measure_number_03():
    r'''Works with implicit time signatures.
    '''

    staff = Staff("c'4 d' e' f' g' a' b' c''")
    staff._update_logical_measure_numbers()

    assert staff._logical_measure_number == 1
    assert staff[0]._logical_measure_number == 1
    assert staff[1]._logical_measure_number == 1
    assert staff[2]._logical_measure_number == 1
    assert staff[3]._logical_measure_number == 1
    assert staff[4]._logical_measure_number == 2
    assert staff[5]._logical_measure_number == 2
    assert staff[6]._logical_measure_number == 2
    assert staff[7]._logical_measure_number == 2


def test_scoretools_Component__logical_measure_number_04():
    r'''Works with a mix of implicit and explicit time signatures.
    '''

    staff = Staff("c'4 d' e' f' g' a' b' c''")
    attach(TimeSignature((2, 4)), staff[4])
    staff._update_logical_measure_numbers()

    assert staff._logical_measure_number == 1
    assert staff[0]._logical_measure_number == 1
    assert staff[1]._logical_measure_number == 1
    assert staff[2]._logical_measure_number == 1
    assert staff[3]._logical_measure_number == 1
    assert staff[4]._logical_measure_number == 2
    assert staff[5]._logical_measure_number == 2
    assert staff[6]._logical_measure_number == 3
    assert staff[7]._logical_measure_number == 3
