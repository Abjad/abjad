from abjad import *


def test_ClefMark_clef_name_01():
    '''Clef name string is read / write.
    '''

    clef = contexttools.ClefMark('treble')
    assert clef.clef_name == 'treble'

    clef.clef_name = 'alto'
    assert clef.clef_name == 'alto'


