from abjad import *
import py.test


def test_NamedChromaticPitchClass___cmp___01():
    '''Referentially equal named pitch-classes compare equally.'''

    npc = pitchtools.NamedChromaticPitchClass('fs')
    assert      npc == npc
    assert not npc != npc
    assert py.test.raises(NotImplementedError, 'npc >  npc')
    assert py.test.raises(NotImplementedError, 'npc >=  npc')
    assert py.test.raises(NotImplementedError, 'npc <  npc')
    assert py.test.raises(NotImplementedError, 'npc <=  npc')


def test_NamedChromaticPitchClass___cmp___02():
    '''Different letter strings.'''

    npc_1 = pitchtools.NamedChromaticPitchClass('fs')
    npc_2 = pitchtools.NamedChromaticPitchClass('gf')

    assert not npc_1 == npc_2
    assert      npc_1 != npc_2
    assert py.test.raises(NotImplementedError, 'npc_1 >  npc_2')
    assert py.test.raises(NotImplementedError, 'npc_1 >=  npc_2')
    assert py.test.raises(NotImplementedError, 'npc_1 <  npc_2')
    assert py.test.raises(NotImplementedError, 'npc_1 <=  npc_2')


def test_NamedChromaticPitchClass___cmp___03():
    '''Same letter strings.'''

    npc_1 = pitchtools.NamedChromaticPitchClass('f')
    npc_2 = pitchtools.NamedChromaticPitchClass('fs')

    assert not npc_1 == npc_2
    assert      npc_1 != npc_2
    assert py.test.raises(NotImplementedError, 'npc_1 >  npc_2')
    assert py.test.raises(NotImplementedError, 'npc_1 >=  npc_2')
    assert py.test.raises(NotImplementedError, 'npc_1 <  npc_2')
    assert py.test.raises(NotImplementedError, 'npc_1 <=  npc_2')
