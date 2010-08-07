from abjad import *


def test_pitchtools_get_pitches_01( ):
   '''Works with containers.'''

   tuplet = FixedDurationTuplet((2, 8), macros.scale(3))
   t = pitchtools.get_pitches(tuplet)

   assert t == (pitchtools.NamedPitch('c', 4), pitchtools.NamedPitch('d', 4), pitchtools.NamedPitch('e', 4))


def test_pitchtools_get_pitches_02( ):
   '''Works with spanners.'''

   staff = Staff(macros.scale(4))
   beam = Beam(staff[:])
   t = pitchtools.get_pitches(beam)

   assert t == (pitchtools.NamedPitch('c', 4), pitchtools.NamedPitch('d', 4), pitchtools.NamedPitch('e', 4), pitchtools.NamedPitch('f', 4))


def test_pitchtools_get_pitches_03( ):
   '''Works with pitch sets.'''

   pitch_set = pitchtools.NamedPitchSet([0, 2, 4, 5])
   t = pitchtools.get_pitches(pitch_set)

   assert t == (pitchtools.NamedPitch('c', 4), pitchtools.NamedPitch('d', 4), pitchtools.NamedPitch('e', 4), pitchtools.NamedPitch('f', 4))


def test_pitchtools_get_pitches_04( ):
   '''Works with pitch arrays.'''

   array = pitchtools.PitchArray([
      [1, (2, 1), (-1.5, 2)],
      [(7, 2), (6, 1), 1],
      ]) 

   '''
   [  ] [d'] [bqf    ]
   [g'     ] [fs'] [ ]
   '''

   assert pitchtools.get_pitches(array) == (
      pitchtools.NamedPitch('d', 4), pitchtools.NamedPitch('bqf', 3), pitchtools.NamedPitch('g', 4), pitchtools.NamedPitch('fs', 4))


def test_pitchtools_get_pitches_05( ):
   '''Works with list or tuple of pitches.'''

   t = [pitchtools.NamedPitch(0), Note(2, (1, 4)), Chord([4, 6, 7], (1, 4))]
   assert pitchtools.get_pitches(t) == (pitchtools.NamedPitch('c', 4), pitchtools.NamedPitch('d', 4), pitchtools.NamedPitch('e', 4), pitchtools.NamedPitch('fs', 4), pitchtools.NamedPitch('g', 4))

