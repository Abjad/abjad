from abjad import *


def test_seqtools_retain_elements_at_indices_01( ):

   g = seqtools.generate_range(20)
   t = list(seqtools.retain_elements_at_indices(g, [1, 16, 17, 18]))
   assert t == [1, 16, 17, 18]


def test_seqtools_retain_elements_at_indices_02( ):

   g = seqtools.generate_range(20)
   t = list(seqtools.retain_elements_at_indices(g, [ ]))
   assert t == [ ]


def test_seqtools_retain_elements_at_indices_03( ):

   g = seqtools.generate_range(20)
   t = list(seqtools.retain_elements_at_indices(g, [99, 100, 101]))
   assert t == [ ]
