from abjad import *
import py.test


def test_NumberedDiatonicPitch___slots___01( ):
   '''Numbered diatonic pitches are immutable.
   '''

   numbered_diatonic_pitch = pitchtools.NumberedDiatonicPitch(7)
   assert py.test.raises(AttributeError, "numbered_diatonic_pitch.foo = 'bar'")
