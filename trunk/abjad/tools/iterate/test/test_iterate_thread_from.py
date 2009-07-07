from abjad import *


def test_iterate_thread_from_01( ):

   container = Container(Voice(construct.run(2)) * 2)
   container.parallel = True
   container[0].name = 'voice 1'
   container[1].name = 'vocie 2'
   staff = Staff(container * 2)
   pitchtools.diatonicize(staff)

   r'''
   \new Staff {
           <<
                   \context Voice = "voice 1" {
                           c'8
                           d'8
                   }
                   \context Voice = "vocie 2" {
                           e'8
                           f'8
                   }
           >>
           <<
                   \context Voice = "voice 1" {
                           g'8
                           a'8
                   }
                   \context Voice = "vocie 2" {
                           b'8
                           c''8
                   }
           >>
   }
   '''

   notes = iterate.thread_from(staff.leaves[0], Note)
   notes = list(notes)

   voice_1_first_half = staff[0][0]
   voice_1_second_half = staff[1][0]

   assert notes[0] is voice_1_first_half[0]
   assert notes[1] is voice_1_first_half[1]
   assert notes[2] is voice_1_second_half[0]
   assert notes[3] is voice_1_second_half[1]


def test_iterate_thread_from_02( ):

   container = Container(Voice(construct.run(2)) * 2)
   container.parallel = True
   container[0].name = 'voice 1'
   container[1].name = 'vocie 2'
   staff = Staff(container * 2)
   pitchtools.diatonicize(staff)

   r'''
   \new Staff {
           <<
                   \context Voice = "voice 1" {
                           c'8
                           d'8
                   }
                   \context Voice = "vocie 2" {
                           e'8
                           f'8
                   }
           >>
           <<
                   \context Voice = "voice 1" {
                           g'8
                           a'8
                   }
                   \context Voice = "vocie 2" {
                           b'8
                           c''8
                   }
           >>
   }
   '''

   components = iterate.thread_from(staff.leaves[0])
   components = list(components)

   r'''
   c'8
   Voice{2}
   d'8
   Voice{2}
   g'8
   a'8
   '''

   assert components[0] is staff.leaves[0]
   assert components[1] is staff[0][0]
   assert components[2] is staff.leaves[1]
   assert components[3] is staff[1][0]
   assert components[4] is staff[1][0][0]
   assert components[5] is staff[1][0][1]
