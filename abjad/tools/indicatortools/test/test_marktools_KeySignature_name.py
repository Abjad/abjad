# -*- encoding: utf-8 -*-
from abjad import *


def test_indicatortools_KeySignature_name_01():

    assert indicatortools.KeySignature('e', 'major').name == 'E major'
    assert indicatortools.KeySignature('E', 'major').name == 'E major'

    assert indicatortools.KeySignature('e', 'minor').name == 'e minor'
    assert indicatortools.KeySignature('E', 'minor').name == 'e minor'
