from abjad import *


def test_pitchtools_leaf_iterables_to_pitch_array_populated_01( ):

   score = Score([ ])
   score.append(Staff(construct.scale(6)))
   score.append(Staff(construct.scale(3, Rational(1, 4))))
   score.append(Staff(construct.scale(6)))

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

   pitch_array = pitchtools.leaf_iterables_to_pitch_array_populated(score)

   '''
   [c'] [d'] [e'] [f'] [g'] [a']
   [c'     ] [d'     ] [e'     ]
   [c'] [d'] [e'] [f'] [g'] [a']
   '''

   assert pitch_array[0].pitches == pitchtools.get_pitches(score[0])
   assert pitch_array[1].pitches == pitchtools.get_pitches(score[1])
   assert pitch_array[2].pitches == pitchtools.get_pitches(score[2])


def test_pitchtools_leaf_iterables_to_pitch_array_populated_02( ):

   score = Score([ ])
   score.append(Staff(construct.scale(4)))
   score.append(Staff(construct.scale(2, Rational(1, 4))))
   score.append(Staff(FixedDurationTuplet((2, 8), construct.scale(3)) * 2))

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

   pitch_array = pitchtools.leaf_iterables_to_pitch_array_populated(score)

   '''
   [c'     ] [d'     ] [e'     ] [f'     ]
   [c'               ] [d'               ]
   [c'] [d'     ] [e'] [c'] [d'     ] [e']
   '''

   assert pitch_array[0].pitches == pitchtools.get_pitches(score[0])
   assert pitch_array[1].pitches == pitchtools.get_pitches(score[1]) 
   assert pitch_array[2].pitches == pitchtools.get_pitches(score[2])
