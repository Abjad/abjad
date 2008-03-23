from abjad import *

def test_container_del_01( ):
   '''Delete 1 Leaf in container. Spanner structure is preserved.'''
   t = Staff(Note(0 , (1,8)) * 4)
   Beam(t)
   del(t[0])
   assert check(t, ret = True)
   assert t.format == "\\new Staff {\n\tc'8 [\n\tc'8\n\tc'8 ]\n}"
   '''
   \new Staff {
        c'8 [
        c'8
        c'8 ]
   }
   ''' 

def test_container_del_02( ):
   '''Delete slice in middle of container.'''
   t = Staff(Note(0, (1, 8)) * 4)
   Beam(t)
   del(t[1:3])
   assert check(t, ret = True)

def test_container_del_03( ):
   '''Delete slice from beginning to middle of container.'''
   t = Staff(Note(0, (1, 8)) * 4)
   Beam(t)
   del(t[0:2])
   assert check(t, ret = True)

def test_container_del_04( ):
   '''Delete slice from middle to end of container.'''
   t = Staff(Note(0, (1, 8)) * 4)
   Beam(t)
   del(t[2:])
   assert check(t, ret = True)

def test_container_del_05( ):
   '''Delete slice from beginning to end of container.'''
   t = Staff(Note(0, (1, 8)) * 4)
   Beam(t)
   del(t[:])
   # No check because empty container is allowed.

def test_container_del_06( ):
   '''Delete Leaf in tuplet preserves spanner.'''
   t = FixedDurationTuplet((1, 4), Note(0 , (1,8)) * 3)
   Beam(t)
   del(t[0])
   assert check(t, ret = True)
   assert t.format =="\tc'8 [\n\tc'8 ]"
   '''
     c'8 [
     c'8 ]
   ''' 
