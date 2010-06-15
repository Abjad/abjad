from abjad import *


def test_check_01( ):
   '''Well-formedness checking runs correctly against leaves.'''
   t = Note(0, (1, 4))
   assert componenttools.is_well_formed_component(t)


def test_check_02( ):
   '''Well-formedness checking runs correctly against containers.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   assert componenttools.is_well_formed_component(t)
