# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_Articulation_name_01():

    a = Articulation('staccato')
    assert a.name == 'staccato'

    a.name = 'marcato'

    assert a.name == 'marcato'
