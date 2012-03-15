from abjad import *
from abjad.tools.pitchtools import NamedChromaticPitch


def test_NamedChromaticPitch___repr___01():
    '''Named chromatic pitch repr is evaluable.
    '''

    named_chromatic_pitch_1 = pitchtools.NamedChromaticPitch("cs''")
    named_chromatic_pitch_2 = eval(repr(named_chromatic_pitch_1))

    '''NamedChromaticPitch("cs''")'''

    assert isinstance(named_chromatic_pitch_1, pitchtools.NamedChromaticPitch)
    assert isinstance(named_chromatic_pitch_2, pitchtools.NamedChromaticPitch)


def test_NamedChromaticPitch___repr___02():
    '''Repr values.
    '''

    named_chromatic_pitch = pitchtools.NamedChromaticPitch("cs''")
    
    assert repr(named_chromatic_pitch) == 'NamedChromaticPitch("cs\'\'")'
    assert named_chromatic_pitch._tools_package_qualified_repr == 'pitchtools.NamedChromaticPitch("cs\'\'")'
    assert named_chromatic_pitch._tools_package_qualified_indented_repr == 'pitchtools.NamedChromaticPitch(\n\t"cs\'\'"\n\t)'
