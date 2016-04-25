# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_KeySignature_name_01():

    assert KeySignature('e', 'major').name == 'E major'
    assert KeySignature('E', 'major').name == 'E major'

    assert KeySignature('e', 'minor').name == 'e minor'
    assert KeySignature('E', 'minor').name == 'e minor'
