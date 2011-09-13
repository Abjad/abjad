from abjad import *


def test_KeySignatureMark_name_01():

    assert contexttools.KeySignatureMark('e', 'major').name == 'E major'
    assert contexttools.KeySignatureMark('E', 'major').name == 'E major'

    assert contexttools.KeySignatureMark('e', 'minor').name == 'e minor'
    assert contexttools.KeySignatureMark('E', 'minor').name == 'e minor'
