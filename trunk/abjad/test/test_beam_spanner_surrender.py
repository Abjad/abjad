from abjad import *


def test_beam_spanner_surrender_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   beam = Beam(t[ : 4])
   assert beam[ : ] == t[ : 4]
   beam.surrender(1)
   assert beam[ : ] == t[ : 3]
   

def test_beam_spanner_surrender_02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   beam = Beam(t[ : 4])
   assert beam[ : ] == t[ : 4]
   beam.surrender(-1)
   assert beam[ : ] == t[1 : 4]
   

def test_beam_spanner_surrender_03( ):
   '''Right-side surrender never equals death.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   beam = Beam(t[ : 4])
   assert beam[ : ] == t[ : 4]
   beam.surrender(99)
   assert beam[ : ] == t[0 : 1]


def test_beam_spanner_surrender_04( ):
   '''Left-side surrender never equals death.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   beam = Beam(t[ : 4])
   assert beam[ : ] == t[ : 4]
   beam.surrender(-99)
   assert beam[ : ] == t[3 : 4]
