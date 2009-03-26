from abjad import *

def test_coalesce_01( ):
   '''coalesce does nothing and returns None on Leaves.'''
   t = Note(1, (1, 4))
   result = coalesce(t)
   assert result is None
   assert isinstance(t, Note)
   

def test_coalesce_02( ):
   '''coalesce will not fuse unnamed voices.'''
   t = Staff([Voice(run(2)), Voice(run(2))])
   result = coalesce(t) 
   assert result is None


def test_coalesce_03( ):
   '''coalesce does not fuse non-threads.'''
   t = Staff([Voice(run(2)), Voice(run(2))])
   t[0].invocation.name = 'one'
   t[1].invocation.name = 'two'
   result = coalesce(t) 
   assert result is None


def test_coalesce_04( ):
   '''coalesce DOES NOT fuse tuplets. '''
   t = Voice([FixedMultiplierTuplet((2, 3), run(3)), 
              FixedMultiplierTuplet((2, 3), run(3))])
   result = coalesce(t)
   assert result is None
   assert len(t) == 2
   

def test_coalesce_05( ):
   '''Coalesce can take a list of components.'''
   t = Voice(run(4)) * 2
   t[0].invocation.name = t[1].invocation.name = 'voiceOne'
   result = coalesce(t)
   assert isinstance(result, Voice)  
   assert len(result) == 8


def test_coalesce_06( ):
   '''Coalesce works on equally named Staves.'''
   t = Staff(run(4)) * 2
   t[0].invocation.name = t[1].invocation.name = 'staffOne'
   result = coalesce(t)
   assert isinstance(result, Staff)  
   assert len(result) == 8


def test_coalesce_07( ):
   '''Coalesce works on equally named Staves but not on differently named
   Voices.'''
   t = Sequential(Staff([Voice(run(4))]) * 2)
   t[0].invocation.name = t[1].invocation.name = 'staffOne'
   r'''
   {
           \context Staff = "staffOne" {
                   \new Voice {
                           c'8
                           c'8
                           c'8
                           c'8
                   }
           }
           \context Staff = "staffOne" {
                   \new Voice {
                           c'8
                           c'8
                           c'8
                           c'8
                   }
           }
   }
   '''
   result = coalesce(t)
   assert isinstance(result, Sequential)  
   assert len(result) == 1
   assert isinstance(result[0], Staff)
   assert len(result[0]) == 2
   assert isinstance(result[0][0], Voice)
   assert isinstance(result[0][1], Voice)
   assert len(result[0][0]) == 4
   assert len(result[0][1]) == 4
   assert result.format == '{\n\t\\context Staff = "staffOne" {\n\t\t\\new Voice {\n\t\t\tc\'8\n\t\t\tc\'8\n\t\t\tc\'8\n\t\t\tc\'8\n\t\t}\n\t\t\\new Voice {\n\t\t\tc\'8\n\t\t\tc\'8\n\t\t\tc\'8\n\t\t\tc\'8\n\t\t}\n\t}\n}'

   r'''
   {
           \context Staff = "staffOne" {
                   \new Voice {
                           c'8
                           c'8
                           c'8
                           c'8
                   }
                   \new Voice {
                           c'8
                           c'8
                           c'8
                           c'8
                   }
           }
   }
'''


## NESTED PARALLEL STRUCTURES ##

def test_coalesce_10( ):
   '''Parallel Voices within parallel Staves within parallel
   StaffGroups within a single Sequential coalesce correctly.'''
   v1 = Voice(Note(0, (1, 4))*2)
   v1.invocation.name = '1'
   v2 = Voice(Note(2, (1, 4))*2)
   v2.invocation.name = '2'
   v3 = Voice(Note(4, (1, 4))*2)
   v3.invocation.name = '3'
   t1 = Staff([v1, v2, v3])
   #t1.brackets = 'double-angle'
   t1.parallel = True
   t1.invocation.name = 'staff1'
   t2 = t1.copy( )
   #t2.brackets = 'double-angle'
   t2.parallel = True
   t2.invocation.name = 'staff2'
   t3 = t1.copy( )
   #t3.brackets = 'double-angle'
   t3.parallel = True
   t3.invocation.name = 'staff3'
   s1 = StaffGroup([t1, t2, t3])
   s1.invocation.name = 'sg'
   s2 = s1.copy( )
   s2.invocation.name = 'sg'
   s = Sequential([s1, s2])

   coalesce(s)
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

def test_coalesce_11( ):
   '''Nested Parallel structures in sequence coalesce correctly.'''
   v1a = Voice(Note(0, (1,4))*2)
   v1a.invocation.name = 'voiceOne'
   v1b = Voice(Note(0, (1,4))*2)
   v1b.invocation.name = 'voiceOne'
   v2a = Voice(Note(12, (1,4))*2)
   v2a.invocation.name = 'voiceTwo'
   v2b = Voice(Note(12, (1,4))*2)
   v2b.invocation.name = 'voiceTwo'
   s1 = Staff([v1a, v1b])
   s1.invocation.name ='staffOne'
   s2 = Staff([v2a, v2b])
   s2.invocation.name ='staffTwo'

   sg1 = StaffGroup([s1, s2])
   sg1.invocation.name ='groupOne'
   sg2 = sg1.copy()
   sg2.invocation.name ='groupTwo'
   sg_g = StaffGroup([sg1, sg2])
   sg_g.invocation.name = 'topGroup'
   seq = coalesce([sg_g, sg_g.copy( )])
   assert seq.format == '\\context StaffGroup = "topGroup" <<\n\t\\context StaffGroup = "groupOne" <<\n\t\t\\context Staff = "staffOne" {\n\t\t\t\\context Voice = "voiceOne" {\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t}\n\t\t}\n\t\t\\context Staff = "staffTwo" {\n\t\t\t\\context Voice = "voiceTwo" {\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t}\n\t\t}\n\t>>\n\t\\context StaffGroup = "groupTwo" <<\n\t\t\\context Staff = "staffOne" {\n\t\t\t\\context Voice = "voiceOne" {\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t}\n\t\t}\n\t\t\\context Staff = "staffTwo" {\n\t\t\t\\context Voice = "voiceTwo" {\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t}\n\t\t}\n\t>>\n>>'

   '''
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
   '''
