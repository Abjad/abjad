from abjad import *
import py.test


def test_container_add_01( ):
   '''Addition DOES NOT works on unnamed voices.'''
   t1 = Voice(Note(0, (1, 4))*2)
   t2 = Voice(Note(0, (1, 4))*2)
   tadd = t1 + t2
   assert tadd is None


def test_container_add_02( ):
   '''Addition DOES NOT work on unnamed Staves.'''
   t1 = Staff(Note(0, (1, 4))*2)
   t2 = Staff(Note(0, (1, 4))*2)
   tadd = t1 + t2
   assert tadd is None


def test_container_add_03( ):
   '''Addition works on simple Containers.'''
   t1 = Container(Note(0, (1, 4))*2)
   t2 = Container(Note(0, (1, 4))*2)
   tadd = t1 + t2
   assert len(tadd) == len(t1) + len(t2)
   assert tadd.format == "{\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n}"
   assert check.wf(tadd)


def test_container_add_04( ):
   '''Addition works on equally named voices.'''
   t1 = Voice(Note(0, (1, 4))*2)
   t1.name = '1'
   t2 = Voice(Note(0, (1, 4))*2)
   t2.name = '1'
   tadd = t1 + t2
   assert len(tadd) == len(t1) + len(t2)
   assert tadd.name == '1'
   assert tadd.format == "\\context Voice = \"1\" {\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n}"


def test_container_add_05( ):
   '''Addition raises exception on differently named voices.'''
   t1 = Voice(Note(0, (1, 4))*2)
   t1.name = '1'
   t2 = Voice(Note(0, (1, 4))*2)
   t2.name = '2'
   assert t1 + t2 is None


def test_container_add_06( ):
   '''Addition works on sequentially nested equally named containers.'''


   t1 = Staff([Voice(Note(0, (1, 4))*2)])
   t2 = Staff([Voice(Note(0, (1, 4))*2)])
   t1[0].name = t2[0].name = 'voiceOne'
   t1.name = t2.name = 'staffOne'
   tadd = t1 + t2
   assert isinstance(tadd, Staff)
   assert len(tadd) == 1
   assert isinstance(tadd[0], Voice)
   assert len(tadd[0]) == 4
   assert tadd.format == '\\context Staff = "staffOne" {\n\t\\context Voice = "voiceOne" {\n\t\tc\'4\n\t\tc\'4\n\t\tc\'4\n\t\tc\'4\n\t}\n}'
 
   r'''
   \context Staff = "staffOne" {
           \context Voice = "voiceOne" {
                   c'4
                   c'4
                   c'4
                   c'4
           }
   }
   '''


### PARALLEL STRUCTURES ###

## NONSTRUCTURAL in new parallel --> context model.
#def test_container_add_10( ):
#   '''Addition raises exception on parallels of notes.'''
#   t1 = Container(Note(0, (1, 4))*2)
#   t1.parallel = True
#   t2 = Container(Note(0, (1, 4))*2)
#   t2.parallel = True
#   assert t1 + t2 is None
    

def test_container_add_11( ):
   '''Addition works on two matching parallel containers each with 
   a single threadable Voice child.'''
   t1 = Container([Voice(Note(0, (1, 4))*2)])
   t1.parallel = True
   t2 = Container([Voice(Note(0, (1, 4))*2)])
   t2.parallel = True
   t1[0].name = t2[0].name = 'voiceOne'
   tadd = t1 + t2
   assert check.wf(tadd)
   assert check.wf(t1)
   assert check.wf(t2)
   assert isinstance(tadd, Container)  
   assert tadd.parallel
   assert len(tadd) == 1
   assert isinstance(tadd[0], Voice)
   assert len(tadd[0]) == 4
    

def test_container_add_13( ): 
   '''Addition works on matching parallel containers each 
   with two named threadable Voice children.'''


   v1 = Voice(Note(0, (1, 4))*2)
   v1.name = '1'
   v2 = Voice(Note(1, (1, 4))*2)
   v2.name = '2'
   v3 = Voice(Note(0, (1, 4))*2)
   v3.name = '1'
   v4 = Voice(Note(1, (1, 4))*2)
   v4.name = '2'
   t1 = Staff([v1, v2])
   t1.parallel = True
   t2 = Staff([v3, v4])
   t2.parallel = True
   t1.name = t2.name = 'staffOne'
   tadd = t1 + t2
   assert isinstance(tadd, Staff)
   assert tadd.parallel
   assert len(tadd) == 2
   assert isinstance(tadd[0], Voice)
   assert isinstance(tadd[1], Voice)
   assert len(tadd[0]) == 4
   assert len(tadd[1]) == 4
   assert tadd[0].name == '1'
   assert tadd[1].name == '2'
   assert tadd.name == 'staffOne'


### iadd ###

def test_container_iadd_01( ):
   '''In place add makes a copy of right hand operand only.'''
   v1 = Voice(Note(1, (1, 4))*4)
   v2 = Voice(Note(2, (1, 4))*4)
   v1.name = v2.name = 'voiceOne'
   v1_id = id(v1)
   v2_id = id(v2)

   v1 += v2
   assert check.wf(v1)
   assert check.wf(v2)
   assert len(v1) == 8
   assert len(v2) == 4
   assert v1.name == 'voiceOne'
   assert v1_id == id(v1)
   assert v2_id == id(v2)
