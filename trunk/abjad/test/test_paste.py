from abjad import *


### TEST EXTEND NOTES ###

def test_extend_notes_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   t.extend(t.copy(0))
   assert check(t, ret = True)

def test_extend_notes_02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   t.extend(t.copy(0, 2))
   assert check(t, ret = True)

def test_extend_notes_03( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   t.extend(t.copy(1, 6))
   assert check(t, ret = True)

def test_extend_notes_04( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   t.extend(t.copy(5, 6))
   assert check(t, ret = True)
