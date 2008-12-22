from abjad import *


def test_beam_spanner_move_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   beam = Beam(t[ : 4])
   #assert beam[ : ] == t[ : 4]
   assert beam.components == t[ : 4]
   beam.move(1)
   #assert beam[ : ] == t[1 : 5]
   assert beam.components == t[1 : 5]


def test_beam_spanner_move_02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   beam = Beam(t[-4 : ])
   #assert beam[ : ] == t[-4 : ]
   assert beam.components == t[-4 : ]
   beam.move(-1)
   #assert beam[ : ] == t[-5 : -1]
   assert beam.components == t[-5 : -1]


def test_beam_spanner_move_03( ):
   '''Move *before first* leaf does nothing.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   beam = Beam(t[ : 4])
   #assert beam[ : ] == t[ : 4]
   assert beam.components == t[ : 4]
   beam.move(-1)
   #assert beam[ : ] == t[ : 4]
   assert beam.components == t[ : 4]


def test_beam_spanner_move_04( ):
   '''Move *beyond last* last does nothing.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   beam = Beam(t[-4 : ])
   #assert beam[ : ] == t[-4 : ]
   assert beam.components == t[-4 : ]
   beam.move(1)
   #assert beam[ : ] == t[-4 : ]
   assert beam.components == t[-4 : ]
