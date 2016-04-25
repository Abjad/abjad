# -*- coding: utf-8 -*-
from abjad import *


def test_selectiontools_LogicalTie_leaves_01():

    staff = Staff("c' ~ c'16")

    assert inspect_(staff[0]).get_logical_tie().leaves == tuple(staff[:])


def test_selectiontools_LogicalTie_leaves_02():

    staff = Staff("c'")

    assert inspect_(staff[0]).get_logical_tie().leaves == (staff[0], )
