from abjad import *


def test_beam_spanner_capture_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   beam = Beam(t[ : 4])
   #assert beam[ : ] == t[ : 4]
   assert beam.components == t[ : 4]
   beam.capture(1)
   #assert beam[ : ] == t[ : 5]
   assert beam.components == t[ : 5]


def test_beam_spanner_capture_02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   beam = Beam(t[-4 : ])
   #assert beam[ : ] == t[-4 : ]
   assert beam.components == t[-4 : ]
   beam.capture(-1)
   #assert beam[ : ] == t[-5 : ]
   assert beam.components == t[-5 : ]


def test_beam_spanner_capture_03( ):
   '''Capturing *before the first* leaf does nothing.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   beam = Beam(t[ : 4])
   #assert beam[ : ] == t[ : 4]
   assert beam.components == t[ : 4]
   beam.capture(-1)
   #assert beam[ : ] == t[ : 4]
   assert beam.components == t[ : 4]


def test_beam_spanner_capture_04( ):
   '''Capturing *past the last* leaf does nothing.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   beam = Beam(t[-4 : ])
   #assert beam[ : ] == t[-4 : ]
   assert beam.components == t[-4 : ]
   beam.capture(1)
   #assert beam[ : ] == t[-4 : ]
   assert beam.components == t[-4 : ]
