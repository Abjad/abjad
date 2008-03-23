from abjad import *


def test_container_insert_01( ):
   '''Insert works just before a spanner.'''
   t = Staff([Note(n, (1, 8)) for n in range(4)])
   Beam(t)
   t.insert(0, Rest((1, 4)))
   assert t.format == "\\new Staff {\n\tr4\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n}"   
   assert check(t, ret = True)
   '''
   \new Staff {
           r4
           c'8 [
           cs'8
           d'8
           ef'8 ]
   }
   '''
   

def test_container_insert_02( ):
   '''Insert works inside a spanner.'''
   t = Staff([Note(n, (1, 8)) for n in range(4)])
   Beam(t)
   t.insert(1, Rest((1, 4)))
   assert t.format == "\\new Staff {\n\tc'8 [ ]\n\tr4\n\tcs'8 [\n\td'8\n\tef'8 ]\n}"
   assert check(t, ret = True)
   '''
   \new Staff {
           c'8 [ ]
           r4
           cs'8 [
           d'8
           ef'8 ]
   }
   '''


def test_container_insert_03( ):
   '''Insert works just after a spanner.'''
   t = Staff([Note(n, (1, 8)) for n in range(4)])
   Beam(t)
   t.insert(4, Rest((1, 4)))
   assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\tr4\n}"
   
   assert check(t, ret = True)
   '''
   \new Staff {
           c'8 [
           cs'8
           d'8
           ef'8 ]
           r4
   }
   '''


def test_container_insert_04( ):
   '''Insert works with really big positive values.'''
   t = Staff([Note(n, (1, 8)) for n in range(4)])
   Beam(t)
   t.insert(1000, Rest((1, 4)))
   assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\tr4\n}"
   
   assert check(t, ret = True)
   '''
   \new Staff {
           c'8 [
           cs'8
           d'8
           ef'8 ]
           r4
   }
   '''


def test_container_insert_05( ):
   '''Insert works with negative values.'''
   t = Staff([Note(n, (1, 8)) for n in range(4)])
   Beam(t)
   t.insert(-1, Rest((1, 4)))
   assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8 ]\n\tr4\n\tef'8 [ ]\n}"
   assert check(t, ret = True)
   '''
   \new Staff {
           c'8 [
           cs'8
           d'8 ]
           r4
           ef'8 [ ]
   }
   '''


def test_container_insert_06( ):
   '''Insert works with really big negative values.'''
   t = Staff([Note(n, (1, 8)) for n in range(4)])
   Beam(t)
   t.insert(-1000, Rest((1, 4)))
   assert t.format == "\\new Staff {\n\tr4\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n}"
  
   assert check(t, ret = True)
   '''
   \new Staff {
           r4
           c'8 [
           cs'8
           d'8
           ef'8 ]
   }
   '''
