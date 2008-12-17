from abjad import *
from py.test import raises

def test_container_add_01( ):
   '''Addition works on simple voices.'''
   t1 = Voice(Note(0, (1, 4))*2)
   t2 = Voice(Note(0, (1, 4))*2)
   tadd = t1 + t2
   assert check(tadd)
   assert check(t1)
   assert check(t2)
   assert len(tadd) == len(t1) + len(t2)
   assert tadd.format == "\\new Voice {\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n}"
   '''
   \new Voice {
           c'4
           c'4
           c'4
           c'4
   }
   '''

def test_container_add_02( ):
   '''Addition works on simple Staves.'''
   t1 = Staff(Note(0, (1, 4))*2)
   t2 = Staff(Note(0, (1, 4))*2)
   tadd = t1 + t2
   assert check(tadd)
   assert check(t1)
   assert check(t2)
   assert len(tadd) == len(t1) + len(t2)
   assert tadd.format == "\\new Staff {\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n}"

def test_container_add_03( ):
   '''Addition works on simple Sequentials.'''
   t1 = Sequential(Note(0, (1, 4))*2)
   t2 = Sequential(Note(0, (1, 4))*2)
   tadd = t1 + t2
   assert len(tadd) == len(t1) + len(t2)
   assert tadd.format == "{\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n}"

def test_container_add_04( ):
   '''Addition works on equally named voices.'''
   t1 = Voice(Note(0, (1, 4))*2)
   t1.invocation.name = 1
   t2 = Voice(Note(0, (1, 4))*2)
   t2.invocation.name = 1
   tadd = t1 + t2
   assert len(tadd) == len(t1) + len(t2)
   assert tadd.invocation.name == 1
   #assert tadd.format == "\\context Voice = \"1\" {\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n}"

def test_container_add_05( ):
   '''Addition raises exception on differently named voices.'''
   t1 = Voice(Note(0, (1, 4))*2)
   t1.invocation.name = 1
   t2 = Voice(Note(0, (1, 4))*2)
   t2.invocation.name = 2
   assert raises(TypeError, 't1 + t2')

def test_container_add_06( ):
   '''Addition works on sequentially nested containers.'''
   t1 = Staff([Voice(Note(0, (1, 4))*2)])
   t2 = Staff([Voice(Note(0, (1, 4))*2)])
   tadd = t1 + t2
   assert isinstance(tadd, Staff)
   assert len(tadd) == 1
   assert isinstance(tadd[0], Voice)
   assert len(tadd[0]) == 4
   assert tadd.format == "\\new Staff {\n\t\\new Voice {\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t}\n}"


### PARALLEL STRUCTURES ###

def test_container_add_10( ):
   '''Addition raises exception on parallels of notes.'''
   t1 = Parallel(Note(0, (1, 4))*2)
   t2 = Parallel(Note(0, (1, 4))*2)
   assert raises(TypeError, 't1 + t2')
    
def test_container_add_11( ):
   '''Addition works on two matching parallel containers each with 
   a single threadable Voice child.'''
   t1 = Parallel([Voice(Note(0, (1, 4))*2)])
   t2 = Parallel([Voice(Note(0, (1, 4))*2)])
   tadd = t1 + t2
   assert check(tadd)
   assert check(t1)
   assert check(t2)
   assert isinstance(tadd, Parallel)  
   assert len(tadd) == 1
   assert isinstance(tadd[0], Voice)
   assert len(tadd[0]) == 4
    

def test_container_add_13( ): 
   '''Addition works on matching parallel containers each 
   with two named threadable Voice children.'''
   v1 = Voice(Note(0, (1, 4))*2)
   v1.invocation.name = 1
   v2 = Voice(Note(1, (1, 4))*2)
   v2.invocation.name = 2
   v3 = Voice(Note(0, (1, 4))*2)
   v3.invocation.name = 1
   v4 = Voice(Note(1, (1, 4))*2)
   v4.invocation.name = 2
   t1 = Staff([v1, v2])
   t1.brackets = 'double-angle'
   t2 = Staff([v3, v4])
   t2.brackets = 'double-angle'
   tadd = t1 + t2
   assert isinstance(tadd, Staff)
   assert tadd.parallel
   assert len(tadd) == 2
   assert isinstance(tadd[0], Voice)
   assert isinstance(tadd[1], Voice)
   assert len(tadd[0]) == 4
   assert len(tadd[1]) == 4
   assert tadd[0].invocation.name == 1
   assert tadd[1].invocation.name == 2


### iadd ###

def test_container_iadd_01( ):
   '''In place add makes a copy of right hand operand only.'''
   v1 = Voice(Note(1, (1, 4))*4)
   v2 = Voice(Note(2, (1, 4))*4)
   v1 += v2
   assert check(v1)
   assert check(v2)
   assert len(v1) == 8
   assert len(v2) == 4
