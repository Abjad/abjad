from abjad import *


def test_listtools_group_by_sign_01( ):

   l = [0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

   t = list(listtools.group_by_sign(l))
   assert t == [[0, 0], [-1, -1], [2, 3], [-5], [1, 2, 5], [-5, -6]]

   t = list(listtools.group_by_sign(l, sign = [-1]))
   assert t == [0, 0, [-1, -1], 2, 3, [-5], 1, 2, 5, [-5, -6]]

   t = list(listtools.group_by_sign(l, sign = [0]))
   assert t == [[0, 0], -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

   t = list(listtools.group_by_sign(l, sign = [1]))
   assert t == [0, 0, -1, -1, [2, 3], -5, [1, 2, 5], -5, -6]

   t = list(listtools.group_by_sign(l, sign = [-1, 0]))
   assert t == [[0, 0], [-1, -1], 2, 3, [-5], 1, 2, 5, [-5, -6]]

   t = list(listtools.group_by_sign(l, sign = [-1, 1]))
   assert t == [0, 0, [-1, -1], [2, 3], [-5], [1, 2, 5], [-5, -6]]

   t = list(listtools.group_by_sign(l, sign = [0, 1]))
   assert t == [[0, 0], -1, -1, [2, 3], -5, [1, 2, 5], -5, -6]

   t = list(listtools.group_by_sign(l, sign = [-1, 0, 1]))
   assert t == [[0, 0], [-1, -1], [2, 3], [-5], [1, 2, 5], [-5, -6]]   
