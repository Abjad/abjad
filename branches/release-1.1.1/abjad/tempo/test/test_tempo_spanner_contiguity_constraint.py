from abjad import *
import py.test


def test_tempo_spanner_contiguity_constraint_01( ):
   '''It is possible to turn off thread-contiguity checking
   for tempo spanners.'''

   staff_chunk = Container(Staff(construct.scale(2)) * 2)
   staff_chunk[0].name = 'foo'
   staff_chunk[1].name = 'bar'
   staff_chunk.parallel = True
   score = Score([ ])
   score.parallel = False
   score.extend(staff_chunk * 2)

   r'''
   \new Score {
           <<
                   \context Staff = "foo" {
                           c'8
                           d'8
                   }
                   \context Staff = "bar" {
                           c'8
                           d'8
                   }
           >>
           <<
                   \context Staff = "foo" {
                           c'8
                           d'8
                   }
                   \context Staff = "bar" {
                           c'8
                           d'8
                   }
           >>
   }
   '''

   assert py.test.raises(ContiguityError, 'Tempo([score[0][0], score[1][0]])')

   tempo = Tempo([ ], TempoIndication(Rational(1, 4), 48))
   tempo._contiguity_constraint = None
   tempo.append(score[0][0])
   tempo.append(score[1][0])

   r'''
   \new Score {
           <<
                   \context Staff = "foo" {
                           \tempo 4=48
                           c'8
                           d'8
                   }
                   \context Staff = "bar" {
                           c'8
                           d'8
                   }
           >>
           <<
                   \context Staff = "foo" {
                           c'8
                           d'8
                           %% tempo 4=48 ends here
                   }
                   \context Staff = "bar" {
                           c'8
                           d'8
                   }
           >>
   }
   '''

   assert check.wf(score)
   assert score.format == '\\new Score {\n\t<<\n\t\t\\context Staff = "foo" {\n\t\t\t\\tempo 4=48\n\t\t\tc\'8\n\t\t\td\'8\n\t\t}\n\t\t\\context Staff = "bar" {\n\t\t\tc\'8\n\t\t\td\'8\n\t\t}\n\t>>\n\t<<\n\t\t\\context Staff = "foo" {\n\t\t\tc\'8\n\t\t\td\'8\n\t\t\t%% tempo 4=48 ends here\n\t\t}\n\t\t\\context Staff = "bar" {\n\t\t\tc\'8\n\t\t\td\'8\n\t\t}\n\t>>\n}' 
   
   

   
