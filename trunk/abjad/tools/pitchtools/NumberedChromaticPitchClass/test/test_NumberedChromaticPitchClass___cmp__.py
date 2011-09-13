from abjad import *
import py.test


def test_NumberedChromaticPitchClass___cmp___01():
    '''Compare unequal numbered chromatic pitch-classes.
    '''

    pc1 = pitchtools.NumberedChromaticPitchClass(6)
    pc2 = pitchtools.NumberedChromaticPitchClass(7)

    assert not pc1 == pc2
    assert      pc1 != pc2

    assert py.test.raises(NotImplementedError, 'pc1 <  pc2')
    assert py.test.raises(NotImplementedError, 'pc1 <= pc2')
    assert py.test.raises(NotImplementedError, 'pc1 >  pc2')
    assert py.test.raises(NotImplementedError, 'pc1 >= pc2')


def test_NumberedChromaticPitchClass___cmp___02():
    '''Compare equal numbered chromatic pitch-classes.
    '''

    pc1 = pitchtools.NumberedChromaticPitchClass(6)
    pc2 = pitchtools.NumberedChromaticPitchClass(6)

    assert      pc1 == pc2
    assert not pc1 != pc2

    assert py.test.raises(NotImplementedError, 'pc1 <  pc2')
    assert py.test.raises(NotImplementedError, 'pc1 <= pc2')
    assert py.test.raises(NotImplementedError, 'pc1 >  pc2')
    assert py.test.raises(NotImplementedError, 'pc1 >= pc2')
