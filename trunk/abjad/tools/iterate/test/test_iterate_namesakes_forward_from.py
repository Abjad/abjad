from abjad import *


def test_iterate_namesakes_forward_from_01( ):

   container = Container(Staff(construct.run(2)) * 2)
   container.parallel = True
   container[0].name = 'staff 1'
   container[1].name = 'staff 2'
   score = Score([ ])
   score.parallel = False
   score.extend(container * 2)
   pitchtools.diatonicize(score)

   r''' 
   \new Score {
           <<
                   \context Staff = "staff 1" {
                           c'8
                           d'8
                   }
                   \context Staff = "staff 2" {
                           e'8
                           f'8
                   }
           >>
           <<
                   \context Staff = "staff 1" {
                           g'8
                           a'8
                   }
                   \context Staff = "staff 2" {
                           b'8
                           c''8
                   }
           >>
   }
   '''

   staves = iterate.namesakes_forward_from(score[0][0])
   staves = list(staves)

   assert staves[0] is score[0][0]
   assert staves[0].name == 'staff 1'

   assert staves[1] is score[1][0]
   assert staves[1].name == 'staff 1'


def test_iterate_namesakes_forward_from_02( ):

   container = Container(Staff(construct.run(2)) * 2)
   container.parallel = True
   container[0].name = 'staff 1'
   container[1].name = 'staff 2'
   score = Score([ ])
   score.parallel = False
   score.extend(container * 2)
   pitchtools.diatonicize(score)

   r''' 
   \new Score {
           <<
                   \context Staff = "staff 1" {
                           c'8
                           d'8
                   }
                   \context Staff = "staff 2" {
                           e'8
                           f'8
                   }
           >>
           <<
                   \context Staff = "staff 1" {
                           g'8
                           a'8
                   }
                   \context Staff = "staff 2" {
                           b'8
                           c''8
                   }
           >>
   }
   '''

   notes = iterate.namesakes_forward_from(score.leaves[0])
   notes = list(notes)

   assert notes[0].staff.effective.name == 'staff 1'
   assert notes[1].staff.effective.name == 'staff 1'
   assert notes[2].staff.effective.name == 'staff 1'
   assert notes[3].staff.effective.name == 'staff 1'
   
