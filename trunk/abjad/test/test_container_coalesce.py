from abjad import *

### NESTED PARALLEL STRUCTURES ###

def test_container_coalesce_01( ):
   '''Parallel Voices within parallel Staves within parallel
   StaffGroups within a single Sequential coalesce correctly.'''
   v1 = Voice(Note(0, (1, 4))*2)
   v1.invocation.name = '1'
   v2 = Voice(Note(2, (1, 4))*2)
   v2.invocation.name = '2'
   v3 = Voice(Note(4, (1, 4))*2)
   v3.invocation.name = '3'
   t1 = Staff([v1, v2, v3])
   t1.brackets = 'double-angle'
   t1.invocation.name = 'staff1'
   t2 = t1.copy( )
   t2.brackets = 'double-angle'
   t2.invocation.name = 'staff2'
   t3 = t1.copy( )
   t3.brackets = 'double-angle'
   t3.invocation.name = 'staff3'
   s1 = StaffGroup([t1, t2, t3])
   s1.invocation.name = 'sg'
   s2 = s1.copy( )
   s2.invocation.name = 'sg'
   s = Sequential([s1, s2])

   s.coalesce( )
   assert len(s) == 1
   assert s.format == '{\n\t\\context StaffGroup = "sg" <<\n\t\t\\context Staff = "staff1" <<\n\t\t\t\\context Voice = "1" {\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t}\n\t\t\t\\context Voice = "2" {\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t}\n\t\t\t\\context Voice = "3" {\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t}\n\t\t>>\n\t\t\\context Staff = "staff2" <<\n\t\t\t\\context Voice = "1" {\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t}\n\t\t\t\\context Voice = "2" {\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t}\n\t\t\t\\context Voice = "3" {\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t}\n\t\t>>\n\t\t\\context Staff = "staff3" <<\n\t\t\t\\context Voice = "1" {\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t}\n\t\t\t\\context Voice = "2" {\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t}\n\t\t\t\\context Voice = "3" {\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t}\n\t\t>>\n\t>>\n}'
 
   '''
   {
        \context StaffGroup = "sg" <<
                \context Staff = "staff1" <<
                        \context Voice = "1" {
                                c'4
                                c'4
                                c'4
                                c'4
                        }
                        \context Voice = "2" {
                                d'4
                                d'4
                                d'4
                                d'4
                        }
                        \context Voice = "3" {
                                e'4
                                e'4
                                e'4
                                e'4
                        }
                >>
                \context Staff = "staff2" <<
                        \context Voice = "1" {
                                c'4
                                c'4
                                c'4
                                c'4
                        }
                        \context Voice = "2" {
                                d'4
                                d'4
                                d'4
                                d'4
                        }
                        \context Voice = "3" {
                                e'4
                                e'4
                                e'4
                                e'4
                        }
                >>
                \context Staff = "staff3" <<
                        \context Voice = "1" {
                                c'4
                                c'4
                                c'4
                                c'4
                        }
                        \context Voice = "2" {
                                d'4
                                d'4
                                d'4
                                d'4
                        }
                        \context Voice = "3" {
                                e'4
                                e'4
                                e'4
                                e'4
                        }
                >>
        >>
   }
   '''

def test_container_coalesce_02( ):
   '''Nested Parallel structures in sequence coalesce correctly.'''
   v1 = Voice(Note(0, (1,4))*2)
   v1.invocation.name = 'voiceOne'
   v2 = Voice(Note(0, (1,4))*2)
   v2.invocation.name = 'voiceOne'
   v3 = Voice(Note(12, (1,4))*2)
   v3.invocation.name = 'voiceTwo'
   v4 = Voice(Note(12, (1,4))*2)
   v4.invocation.name = 'voiceTwo'
   s1 = Staff([v1, v2])
   s1.invocation.name ='staffOne'
   s2 = Staff([v3, v4])
   s2.invocation.name ='staffTwo'

   sg1 = StaffGroup([s1, s2])
   sg1.invocation.name ='groupOne'
   sg2 = sg1.copy()
   sg2.invocation.name ='groupTwo'
   sg_g = StaffGroup([sg1, sg2])
   sg_g.invocation.name = 'topGroup'
   seq = Sequential([sg_g, sg_g.copy( )])
   seq.coalesce( )
   assert len(seq) == 1
   assert seq.format == '{\n\t\\context StaffGroup = "topGroup" <<\n\t\t\\context StaffGroup = "groupOne" <<\n\t\t\t\\context Staff = "staffOne" {\n\t\t\t\t\\context Voice = "voiceOne" {\n\t\t\t\t\tc\'4\n\t\t\t\t\tc\'4\n\t\t\t\t\tc\'4\n\t\t\t\t\tc\'4\n\t\t\t\t\tc\'4\n\t\t\t\t\tc\'4\n\t\t\t\t\tc\'4\n\t\t\t\t\tc\'4\n\t\t\t\t}\n\t\t\t}\n\t\t\t\\context Staff = "staffTwo" {\n\t\t\t\t\\context Voice = "voiceTwo" {\n\t\t\t\t\tc\'\'4\n\t\t\t\t\tc\'\'4\n\t\t\t\t\tc\'\'4\n\t\t\t\t\tc\'\'4\n\t\t\t\t\tc\'\'4\n\t\t\t\t\tc\'\'4\n\t\t\t\t\tc\'\'4\n\t\t\t\t\tc\'\'4\n\t\t\t\t}\n\t\t\t}\n\t\t>>\n\t\t\\context StaffGroup = "groupTwo" <<\n\t\t\t\\context Staff = "staffOne" {\n\t\t\t\t\\context Voice = "voiceOne" {\n\t\t\t\t\tc\'4\n\t\t\t\t\tc\'4\n\t\t\t\t\tc\'4\n\t\t\t\t\tc\'4\n\t\t\t\t\tc\'4\n\t\t\t\t\tc\'4\n\t\t\t\t\tc\'4\n\t\t\t\t\tc\'4\n\t\t\t\t}\n\t\t\t}\n\t\t\t\\context Staff = "staffTwo" {\n\t\t\t\t\\context Voice = "voiceTwo" {\n\t\t\t\t\tc\'\'4\n\t\t\t\t\tc\'\'4\n\t\t\t\t\tc\'\'4\n\t\t\t\t\tc\'\'4\n\t\t\t\t\tc\'\'4\n\t\t\t\t\tc\'\'4\n\t\t\t\t\tc\'\'4\n\t\t\t\t\tc\'\'4\n\t\t\t\t}\n\t\t\t}\n\t\t>>\n\t>>\n}'

   '''
   {
           \context StaffGroup = "topGroup" <<
                   \context StaffGroup = "groupOne" <<
                           \context Staff = "staffOne" {
                                   \context Voice = "voiceOne" {
                                           c'4
                                           c'4
                                           c'4
                                           c'4
                                           c'4
                                           c'4
                                           c'4
                                           c'4
                                   }
                           }
                           \context Staff = "staffTwo" {
                                   \context Voice = "voiceTwo" {
                                           c''4
                                           c''4
                                           c''4
                                           c''4
                                           c''4
                                           c''4
                                           c''4
                                           c''4
                                   }
                           }
                   >>
                   \context StaffGroup = "groupTwo" <<
                           \context Staff = "staffOne" {
                                   \context Voice = "voiceOne" {
                                           c'4
                                           c'4
                                           c'4
                                           c'4
                                           c'4
                                           c'4
                                           c'4
                                           c'4
                                   }
                           }
                           \context Staff = "staffTwo" {
                                   \context Voice = "voiceTwo" {
                                           c''4
                                           c''4
                                           c''4
                                           c''4
                                           c''4
                                           c''4
                                           c''4
                                           c''4
                                   }
                           }
                   >>
           >>
   }
   '''


