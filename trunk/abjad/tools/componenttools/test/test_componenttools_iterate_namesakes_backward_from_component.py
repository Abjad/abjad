from abjad import *
import py.test


def test_componenttools_iterate_namesakes_backward_from_component_01( ):

   container = Container(Staff(leaftools.make_repeated_notes(2)) * 2)
   container.parallel = True
   container[0].name = 'staff 1'
   container[1].name = 'staff 2'
   score = Score([ ])
   score.parallel = False
   score.extend(container * 2)
   pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr(score)

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

   staves = componenttools.iterate_namesakes_backward_from_component(score[1][0])
   staves = list(staves)

   assert staves[0] is score[1][0]
   assert staves[0].name == 'staff 1'

   assert staves[1] is score[0][0]
   assert staves[1].name == 'staff 1'


def test_componenttools_iterate_namesakes_backward_from_component_02( ):

   container = Container(Staff(leaftools.make_repeated_notes(2)) * 2)
   container.parallel = True
   container[0].name = 'staff 1'
   container[1].name = 'staff 2'
   score = Score([ ])
   score.parallel = False
   score.extend(container * 2)
   pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr(score)

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

   notes = componenttools.iterate_namesakes_backward_from_component(score.leaves[-1])
   notes = list(notes)

   r'''
   Note(c'', 8)
   Note(b', 8)
   Note(f', 8)
   Note(e', 8)
   '''

   assert notes[0].staff.effective.name == 'staff 2'
   assert notes[1].staff.effective.name == 'staff 2'
   assert notes[2].staff.effective.name == 'staff 2'
   assert notes[3].staff.effective.name == 'staff 2'
   


def test_componenttools_iterate_namesakes_backward_from_component_03( ):
   '''Optional start and stop keywords.'''

   t = Staff(FixedDurationTuplet((2, 8), leaftools.make_repeated_notes(3)) * 2)
   pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

   r'''
   \new Staff {
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

   g = componenttools.iterate_namesakes_backward_from_component(t.leaves[-2], 0, 3)

   assert g.next( ) is t.leaves[-2]
   assert g.next( ) is t.leaves[-3]
   assert g.next( ) is t.leaves[-4]
   assert py.test.raises(StopIteration, 'g.next( )')


def test_componenttools_iterate_namesakes_backward_from_component_04( ):
   '''Optional start and stop keywords.'''

   t = Staff(FixedDurationTuplet((2, 8), leaftools.make_repeated_notes(3)) * 2)
   pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

   r'''
   \new Staff {
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

   g = componenttools.iterate_namesakes_backward_from_component(t.leaves[-2], 2)

   assert g.next( ) is t.leaves[-4]
   assert g.next( ) is t.leaves[-5]
   assert g.next( ) is t.leaves[-6]
   assert py.test.raises(StopIteration, 'g.next( )')
