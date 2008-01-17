from abjad import *


def test_tester_01( ):
   '''Tester runs correctly against leaves.'''
   t = Note(0, (1, 4))
   assert t.tester.testAll(ret = True)


def test_tester_02( ):
   '''Tester runs correctly against containers.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   assert t.tester.testAll(ret = True)
