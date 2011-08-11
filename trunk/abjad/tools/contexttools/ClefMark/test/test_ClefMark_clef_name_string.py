from abjad import *


def test_ClefMark_clef_name_string_01( ):
    '''Clef name string is read / write.
    '''

    clef = contexttools.ClefMark('treble')
    assert clef.clef_name_string == 'treble'

    clef.clef_name_string = 'alto'
    assert clef.clef_name_string == 'alto'


