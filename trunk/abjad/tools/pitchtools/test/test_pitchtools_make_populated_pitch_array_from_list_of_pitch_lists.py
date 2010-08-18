from abjad import *


def test_pitchtools_make_populated_pitch_array_from_list_of_pitch_lists_01( ):

   score = Score([ ])
   score.append(Staff(macros.scale(6)))
   score.append(Staff(macros.scale(3, Rational(1, 4))))
   score.append(Staff(macros.scale(6)))

   r'''
   \new Score <<
           \new Staff {
                   c'8
                   d'8
                   e'8
                   f'8
                   g'8
                   a'8
           }
           \new Staff {
                   c'4
                   d'4
                   e'4
           }
           \new Staff {
                   c'8
                   d'8
                   e'8
                   f'8
                   g'8
                   a'8
           }
   >>
   '''

   pitch_array = pitchtools.make_populated_pitch_array_from_list_of_pitch_lists(score)

   '''
   [c'] [d'] [e'] [f'] [g'] [a']
   [c'     ] [d'     ] [e'     ]
   [c'] [d'] [e'] [f'] [g'] [a']
   '''

   assert pitch_array[0].pitches == pitchtools.list_named_pitches_in_expr(score[0])
   assert pitch_array[1].pitches == pitchtools.list_named_pitches_in_expr(score[1])
   assert pitch_array[2].pitches == pitchtools.list_named_pitches_in_expr(score[2])


def test_pitchtools_make_populated_pitch_array_from_list_of_pitch_lists_02( ):

   score = Score([ ])
   score.append(Staff(macros.scale(4)))
   score.append(Staff(macros.scale(2, Rational(1, 4))))
   score.append(Staff(tuplettools.FixedDurationTuplet((2, 8), macros.scale(3)) * 2))

   r'''
   \new Score <<
           \new Staff {
                   c'8
                   d'8
                   e'8
                   f'8
           }
           \new Staff {
                   c'4
                   d'4
           }
           \new Staff {
                   \times 2/3 {
                           c'8
                           d'8
                           e'8
                   }
                   \times 2/3 {
                           c'8
                           d'8
                           e'8
                   }
           }
   >>
   '''

   pitch_array = pitchtools.make_populated_pitch_array_from_list_of_pitch_lists(score)

   '''
   [c'     ] [d'     ] [e'     ] [f'     ]
   [c'               ] [d'               ]
   [c'] [d'     ] [e'] [c'] [d'     ] [e']
   '''

   assert pitch_array[0].pitches == pitchtools.list_named_pitches_in_expr(score[0])
   assert pitch_array[1].pitches == pitchtools.list_named_pitches_in_expr(score[1]) 
   assert pitch_array[2].pitches == pitchtools.list_named_pitches_in_expr(score[2])
