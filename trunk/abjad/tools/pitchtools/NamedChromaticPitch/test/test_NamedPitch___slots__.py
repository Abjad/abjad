from abjad import *
import py.test


def test_NamedPitch___slots___01( ):

   named_chromatic_pitch = pitchtools.NamedChromaticPitch("cs''")
   assert py.test.raises(AttributeError, "named_chromatic_pitch.foo = 'bar'")
