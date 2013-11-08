# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_KeySignature_name_01():

    assert marktools.KeySignature('e', 'major').name == 'E major'
    assert marktools.KeySignature('E', 'major').name == 'E major'

    assert marktools.KeySignature('e', 'minor').name == 'e minor'
    assert marktools.KeySignature('E', 'minor').name == 'e minor'
