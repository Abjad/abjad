from abjad import *


### TEST EXTEND NOTES ###

def test_extend_notes_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   #t.extend(t.copy(0))
   t.extend(tcopy(t[0 : 1]))
   assert check(t, ret = True)

def test_extend_notes_02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   #t.extend(t.copy(0, 2))
   t.extend(tcopy(t[0 : 3]))
   assert check(t, ret = True)

def test_extend_notes_03( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   #t.extend(t.copy(1, 6))
   t.extend(tcopy(t[1 : 7]))
   assert check(t, ret = True)

def test_extend_notes_04( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   #t.extend(t.copy(5, 6))
   t.extend(tcopy(t[5 : 7]))
   assert check(t, ret = True)
