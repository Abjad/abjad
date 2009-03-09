from abjad import *


def test_container_hew_01( ):
   '''Hew triplet.'''

   t = Voice(FixedDurationTuplet((2, 8), run(3)) * 2)
   diatonicize(t)
   p = Beam(t[:])

   r'''
   \new Voice {
           \times 2/3 {
                   c'8
                   d'8
                   e'8
           }
           \times 2/3 {
                   f'8
                   g'8
                   a'8
           }
   }
   '''

   container_hew(t[1], 1)

   r'''\new Voice {
           \times 2/3 {
                   c'8 [
                   d'8
                   e'8
           }
           \times 2/3 {
                   f'8
           }
           \times 2/3 {
                   g'8
                   a'8 ]
           }
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tf'8\n\t}\n\t\\times 2/3 {\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"


def test_container_hew_02( ):
   '''Hew binary measure.'''

   t = Voice(RigidMeasure((3, 8), run(3)) * 2)
   diatonicize(t)
   p = Beam(t[:])

   r'''
   \new Voice {
                   \time 3/8
                   c'8 [
                   d'8
                   e'8
                   \time 3/8
                   f'8
                   g'8
                   a'8 ]
   }
   '''

   container_hew(t[1], 1)

   r'''
   \new Voice {
                   \time 3/8
                   c'8 [
                   d'8
                   e'8
                   \time 1/8
                   f'8
                   \time 2/8
                   g'8
                   a'8 ]
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\t\t\\time 3/8\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t\t\\time 1/8\n\t\tf'8\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8 ]\n}"


def test_container_hew_03( ):
   '''Hew nonbinary measure.'''

   t = Voice(RigidMeasure((3, 9), run(3)) * 2)
   diatonicize(t)
   p = Beam(t[:])

   r'''
   \new Voice {
                   \time 3/9
                   \scaleDurations #'(8 . 9) {
                           c'8 [
                           d'8
                           e'8
                   }
                   \time 3/9
                   \scaleDurations #'(8 . 9) {
                           f'8
                           g'8
                           a'8 ]
                   }
   }
   '''

   container_hew(t[1], 1)

   r'''
   \new Voice {
                   \time 3/9
                   \scaleDurations #'(8 . 9) {
                           c'8 [
                           d'8
                           e'8
                   }
                   \time 1/9
                   \scaleDurations #'(8 . 9) {
                           f'8
                   }
                   \time 2/9
                   \scaleDurations #'(8 . 9) {
                           g'8
                           a'8 ]
                   }
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\t\t\\time 3/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tc'8 [\n\t\t\td'8\n\t\t\te'8\n\t\t}\n\t\t\\time 1/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tf'8\n\t\t}\n\t\t\\time 2/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tg'8\n\t\t\ta'8 ]\n\t\t}\n}"


def test_container_hew_04( ):
   '''A single container can be split in two by the middle;
      no parent.'''

   t = Voice(scale(4))
   t1, t2 = container_hew(t, 2)

   r'''
   \new Voice {
      c'8
      d'8
   }
   \new Voice {
      e'8
      f'8
   }
   '''

   assert check(t1)
   assert check(t2)
   assert t1.format == "\\new Voice {\n\tc'8\n\td'8\n}"
   assert t2.format == "\\new Voice {\n\te'8\n\tf'8\n}"
   

def test_container_hew_05( ):
   '''A single container 'split' at index 0 is unmodified.'''

   t = Voice(scale(4))
   t1, t2 = container_hew(t, 0)

   r'''
   \new Voice {
   }
   \new Voice {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert check(t2)
   assert t1.format == '\\new Voice {\n}'
   assert t2.format == "\\new Voice {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


## TODO: Update all tests here to work correctly;
##       make good corner case checks for container_hew( );
##       after updated, rename container_splinter( ) to container_split( ).

#def test_container_hew_06( ):
#   '''
#   A single container 'split' at index > len(container) is unmodified.
#   '''
#   t = Voice(run(4))
#   t1, t2 = container_hew(t, 10)
#   assert len(t1) == 4
#   assert t1 is t
#   assert t2 is None
#
#
#def test_container_hew_07( ):
#   '''
#   A single container can be split with negative indeces.
#   '''
#   t = Voice(run(4))
#   t1, t2 = container_hew(t, -2)
#   assert len(t1) == len(t2) == 2
#   assert t[0] is t1[0]
#   assert t1 is t
#
#   t = Voice(run(4))
#   t1, t2 = container_hew(t, -1)
#   assert len(t1) == 3
#   assert len(t2) == 1
#   assert t[0] is t1[0]
#   assert t1 is t
#
#
#### NESTED CONTAINERS ###
#
#def test_conatiner_split_08( ):
#   '''
#   Splitting a container with parent results in parented brother
#   split containers.
#   '''
#   t = Staff([Voice(run(4))])
#   t1, t2 = container_hew(t[0], 2)
#   assert t1._parent is t
#   assert t2._parent is t
#   assert len(t1) == len(t2) == 2
#   assert len(t) == 2
#   assert t1 is t[0]
#   assert t2 is t[1]
#
#
#### SPANNERS ###
#
#def test_container_hew_09( ):
#   '''
#   Spanners attached to split container are copied. 
#   '''
#   t = Staff([Voice(run(4))])
#   Beam(t[:])
#   t1, t2 = container_hew(t[0], 2)
#   assert t1.beam.spanner
#   assert t2.beam.spanner
#   assert not t1.beam.spanner is t2.beam.spanner
#   assert t.format == "\\new Staff {\n\t\\new Voice {\n\t\tc'8 [\n\t\tc'8 ]\n\t}\n\t\\new Voice {\n\t\tc'8 [\n\t\tc'8 ]\n\t}\n}"
#
#   '''
#   \new Staff {
#           \new Voice {
#                   c'8 [
#                   c'8 ]
#           }
#           \new Voice {
#                   c'8 [
#                   c'8 ]
#           }
#   }
#   '''  
#
#
#def test_container_hew_10( ):
#   '''
#   Splitting a container with parent results in parented brother
#   split containers.
#   '''
#   t = Staff([Voice([FixedMultiplierTuplet((4,5), run(5))])])
#   voice = t[0]
#   tuplet = voice[0]
#   Beam(tuplet)
#   t1, t2 = container_hew(tuplet, 2)
#   assert t1._parent is voice
#   assert t2._parent is voice
#   assert len(t1) == 2
#   assert len(t2) == 3
#   assert len(voice) == 2
#   assert t1 is voice[0]
#   assert t2 is voice[1]
#   assert t1.beam.spanner
#   assert t2.beam.spanner
#   assert t1.beam.spanner is not t2.beam.spanner
#   assert check(t)
#   assert t.format == "\\new Staff {\n\t\\new Voice {\n\t\t\\times 4/5 {\n\t\t\tc'8 [\n\t\t\tc'8 ]\n\t\t}\n\t\t\\times 4/5 {\n\t\t\tc'8 [\n\t\t\tc'8\n\t\t\tc'8 ]\n\t\t}\n\t}\n}"
#   '''
#   \new Staff {
#           \new Voice {
#                   \times 4/5 {
#                           c'8 [
#                           c'8 ]
#                   }
#                   \times 4/5 {
#                           c'8 [
#                           c'8
#                           c'8 ]
#                   }
#           }
#   }
#   '''

