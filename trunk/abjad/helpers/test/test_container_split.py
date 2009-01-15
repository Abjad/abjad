from abjad import *

def test_container_split_01( ):
   '''
   A single container can be split in two by the middle.
   '''
   t = Voice(run(4))
   t1, t2 = container_split(t, 2)
   assert len(t1) == len(t2) == 2
   assert id(t1) != id(t2)
   assert t1 is t
   

def test_container_split_02( ):
   '''
   A single container 'split' at index 0 is unmodified.
   '''
   t = Voice(run(4))
   t1, t2 = container_split(t, 0)
   assert len(t1) == 4
   assert t1 is t
   assert t2 is None


def test_container_split_03( ):
   '''
   A single container 'split' at index > len(container) is unmodified.
   '''
   t = Voice(run(4))
   t1, t2 = container_split(t, 10)
   assert len(t1) == 4
   assert t1 is t
   assert t2 is None


def test_container_split_04( ):
   '''
   A single container can be split with negative indeces.
   '''
   t = Voice(run(4))
   t1, t2 = container_split(t, -2)
   assert len(t1) == len(t2) == 2
   assert t[0] is t1[0]
   assert t1 is t

   t = Voice(run(4))
   t1, t2 = container_split(t, -1)
   assert len(t1) == 3
   assert len(t2) == 1
   assert t[0] is t1[0]
   assert t1 is t


### NESTED CONTAINERS ###

def test_conatiner_split_05( ):
   '''
   Splitting a container with parent results in parented brother
   split containers.
   '''
   t = Staff([Voice(run(4))])
   t1, t2 = container_split(t[0], 2)
   assert t1._parent is t
   assert t2._parent is t
   assert len(t1) == len(t2) == 2
   assert len(t) == 2
   assert t1 is t[0]
   assert t2 is t[1]


### SPANNERS ###

def test_container_split_06( ):
   '''
   Spanners attached to split container are copied. 
   '''
   t = Staff([Voice(run(4))])
   Beam(t[:])
   t1, t2 = container_split(t[0], 2)
   assert t1.beam.spanner
   assert t2.beam.spanner
   assert not t1.beam.spanner is t2.beam.spanner
   assert t.format == "\\new Staff {\n\t\\new Voice {\n\t\tc'8 [\n\t\tc'8 ]\n\t}\n\t\\new Voice {\n\t\tc'8 [\n\t\tc'8 ]\n\t}\n}"

   '''
   \new Staff {
           \new Voice {
                   c'8 [
                   c'8 ]
           }
           \new Voice {
                   c'8 [
                   c'8 ]
           }
   }
   '''  


def test_container_split_07( ):
   '''
   Splitting a container with parent results in parented brother
   split containers.
   '''
   t = Staff([Voice([FixedMultiplierTuplet((4,5), run(5))])])
   voice = t[0]
   tuplet = voice[0]
   Beam(tuplet)
   t1, t2 = container_split(tuplet, 2)
   assert t1._parent is voice
   assert t2._parent is voice
   assert len(t1) == 2
   assert len(t2) == 3
   assert len(voice) == 2
   assert t1 is voice[0]
   assert t2 is voice[1]
   assert t1.beam.spanner
   assert t2.beam.spanner
   assert t1.beam.spanner is not t2.beam.spanner
   assert check(t)
   assert t.format == "\\new Staff {\n\t\\new Voice {\n\t\t\\times 4/5 {\n\t\t\tc'8 [\n\t\t\tc'8 ]\n\t\t}\n\t\t\\times 4/5 {\n\t\t\tc'8 [\n\t\t\tc'8\n\t\t\tc'8 ]\n\t\t}\n\t}\n}"
   '''
   \new Staff {
           \new Voice {
                   \times 4/5 {
                           c'8 [
                           c'8 ]
                   }
                   \times 4/5 {
                           c'8 [
                           c'8
                           c'8 ]
                   }
           }
   }
   '''
