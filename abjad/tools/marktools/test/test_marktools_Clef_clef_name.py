# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_Clef_clef_name_01():
    r'''Clef name is read / write.
    '''

    clef = Clef('treble')
    assert clef.clef_name == 'treble'

    clef.clef_name = 'alto'
    assert clef.clef_name == 'alto'
