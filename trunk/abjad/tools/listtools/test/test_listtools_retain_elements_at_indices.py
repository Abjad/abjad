from abjad import *


def test_listtools_retain_elements_at_indices_01( ):

   g = listtools._generator(20)
   t = list(listtools.retain_elements_at_indices(g, [1, 16, 17, 18]))
   assert t == [1, 16, 17, 18]


def test_listtools_retain_elements_at_indices_02( ):

   g = listtools._generator(20)
   t = list(listtools.retain_elements_at_indices(g, [ ]))
   assert t == [ ]


def test_listtools_retain_elements_at_indices_03( ):

   g = listtools._generator(20)
   t = list(listtools.retain_elements_at_indices(g, [99, 100, 101]))
   assert t == [ ]
