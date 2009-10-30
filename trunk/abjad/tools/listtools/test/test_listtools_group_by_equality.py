from abjad import *


def test_listtools_group_by_equality_01( ):

   l = [ ]

   t = list(listtools.group_by_equality(l))
   assert t == [ ]


def test_listtools_group_by_equality_02( ):

   l = [1, 1, 1, 'a', 'a']

   t = list(listtools.group_by_equality(l))
   assert t == [(1, 1, 1), ('a', 'a')]


def test_listtools_group_by_equality_03( ):

   l = [0, 0, -1, -1, 2, 3, -5, 1, 1, 5, -5]

   t = list(listtools.group_by_equality(l))
   assert t == [(0, 0), (-1, -1), (2,), (3,), (-5,), (1, 1), (5,), (-5,)]
