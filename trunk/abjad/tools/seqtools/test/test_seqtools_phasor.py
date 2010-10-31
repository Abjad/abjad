from abjad import *
import types

def test_seqtools_phasor_01( ):
   '''Defaults step to 1 and start to 0.'''

   l = [1, 2, 3, 4, 5, 6, 7]
   t = list(seqtools.phasor(l, length = 20))

   assert t == [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6]


def test_seqtools_phasor_02( ):
   '''Step can be greater than 1.'''

   l = [1, 2, 3, 4, 5, 6, 7]
   t = list(seqtools.phasor(l, 2, length = 20))

   assert t == [1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4]


def test_seqtools_phasor_03( ):
   '''Start can be greater than 0.'''

   l = [1, 2, 3, 4, 5, 6, 7]
   t = list(seqtools.phasor(l, 2, 3, length = 20))

   assert t == [4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7]


def test_seqtools_phasor_04( ):
   '''Step can be negative.'''

   l = [1, 2, 3, 4, 5, 6, 7]
   t = list(seqtools.phasor(l, -2, 5, length = 20))

   assert t == [6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3]


def test_seqtools_phasor_05( ):
   '''Works on generator input.'''

   g = seqtools.generate_range(1, 8)
   t = list(seqtools.phasor(g, length = 20))
   assert t == [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6]

   g = seqtools.generate_range(1, 8)
   t = list(seqtools.phasor(g, 2, length = 20))
   assert t == [1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4]

   g = seqtools.generate_range(1, 8)
   t = list(seqtools.phasor(g, 2, 3, length = 20))
   assert t == [4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7]

   g = seqtools.generate_range(1, 8)
   t = list(seqtools.phasor(g, -2, 5, length = 20))
   assert t == [6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3]
