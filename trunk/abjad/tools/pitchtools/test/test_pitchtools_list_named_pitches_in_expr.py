from abjad import *


def test_pitchtools_list_named_pitches_in_expr_01( ):
   '''Works with containers.'''

   tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
   t = pitchtools.list_named_pitches_in_expr(tuplet)

   assert t == (pitchtools.NamedPitch('c', 4), pitchtools.NamedPitch('d', 4), pitchtools.NamedPitch('e', 4))


def test_pitchtools_list_named_pitches_in_expr_02( ):
   '''Works with spanners.'''

   staff = Staff(macros.scale(4))
   beam = spannertools.BeamSpanner(staff[:])
   t = pitchtools.list_named_pitches_in_expr(beam)

   assert t == (pitchtools.NamedPitch('c', 4), pitchtools.NamedPitch('d', 4), pitchtools.NamedPitch('e', 4), pitchtools.NamedPitch('f', 4))


def test_pitchtools_list_named_pitches_in_expr_03( ):
   '''Works with pitch sets.'''

   pitch_set = pitchtools.NamedPitchSet([0, 2, 4, 5])
   t = pitchtools.list_named_pitches_in_expr(pitch_set)

   assert t == (pitchtools.NamedPitch('c', 4), pitchtools.NamedPitch('d', 4), pitchtools.NamedPitch('e', 4), pitchtools.NamedPitch('f', 4))


def test_pitchtools_list_named_pitches_in_expr_04( ):
   '''Works with pitch arrays.'''

   array = pitchtools.PitchArray([
      [1, (2, 1), (-1.5, 2)],
      [(7, 2), (6, 1), 1],
      ]) 

   '''
   [  ] [d'] [bqf    ]
   [g'     ] [fs'] [ ]
   '''

   assert pitchtools.list_named_pitches_in_expr(array) == (
      pitchtools.NamedPitch('d', 4), pitchtools.NamedPitch('bqf', 3), pitchtools.NamedPitch('g', 4), pitchtools.NamedPitch('fs', 4))


def test_pitchtools_list_named_pitches_in_expr_05( ):
   '''Works with list or tuple of pitches.'''

   t = [pitchtools.NamedPitch(0), Note(2, (1, 4)), Chord([4, 6, 7], (1, 4))]
   assert pitchtools.list_named_pitches_in_expr(t) == (pitchtools.NamedPitch('c', 4), pitchtools.NamedPitch('d', 4), pitchtools.NamedPitch('e', 4), pitchtools.NamedPitch('fs', 4), pitchtools.NamedPitch('g', 4))

