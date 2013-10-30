# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_KeySignatureMark_name_01():

    assert marktools.KeySignatureMark('e', 'major').name == 'E major'
    assert marktools.KeySignatureMark('E', 'major').name == 'E major'

    assert marktools.KeySignatureMark('e', 'minor').name == 'e minor'
    assert marktools.KeySignatureMark('E', 'minor').name == 'e minor'
