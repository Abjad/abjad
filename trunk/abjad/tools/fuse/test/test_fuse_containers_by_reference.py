from abjad import *
import py.test


def test_fuse_containers_by_reference_01( ):
   '''Do nothing on leaf.'''

   t = Note(1, (1, 4))
   result = fuse.containers_by_reference(t)
   assert result is None
   assert isinstance(t, Note)
   

def test_fuse_containers_by_reference_02( ):
   '''Do not fuse unnamed voices.'''

   t = Staff([Voice(construct.run(2)), Voice(construct.run(2))])
   result = fuse.containers_by_reference(t) 
   assert result is None


def test_fuse_containers_by_reference_03( ):
   '''Do not fuse nonthreads.'''

   t = Staff([Voice(construct.run(2)), Voice(construct.run(2))])
   t[0].name = 'one'
   t[1].name = 'two'
   result = fuse.containers_by_reference(t) 
   assert result is None


def test_fuse_containers_by_reference_04( ):
   '''Do not fuse tuplets.'''

   t = Voice([FixedMultiplierTuplet((2, 3), construct.run(3)), 
              FixedMultiplierTuplet((2, 3), construct.run(3))])
   result = fuse.containers_by_reference(t)
   assert result is None
   assert len(t) == 2
   

def test_fuse_containers_by_reference_05( ):
   '''Fuse like-named staves.'''

   t = Staff(construct.run(4)) * 2
   t[0].name = t[1].name = 'staffOne'
   result = fuse.containers_by_reference(t)
   assert isinstance(result, Staff)  
   assert len(result) == 8


def test_fuse_containers_by_reference_06( ):
   '''Fuse like-named staves but not differently named voices.'''

   t = Container(Staff([Voice(construct.run(4))]) * 2)
   t[0].name = t[1].name = 'staffOne'

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

   result = fuse.containers_by_reference(t)
   assert isinstance(result, Container)  
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


def test_fuse_containers_by_reference_07( ):
   '''Fuse orphan components.'''

   t = Voice(construct.run(4)) * 2
   t[0].name = t[1].name = 'voiceOne'
   result = fuse.containers_by_reference(t)
   assert isinstance(result, Voice)  
   assert len(result) == 8


## TODO this should work.
#def test_fuse_containers_by_reference_08( ):
#   '''fuse.containers_by_reference( ) can take a list of parented 
#   Components.'''
#   t = Staff(Voice(construct.run(2)) * 2)
#   result = fuse.containers_by_reference(t[:])
#   assert check.wf(t)
#   assert len(t) == 1


## NESTED PARALLEL STRUCTURES ##

def test_fuse_containers_by_reference_09( ):
   '''Fuse parallel voices within parallel staves within parallel
   staff groups within a single container.
   '''

   v1 = Voice(Note(0, (1, 4))*2)
   v1.name = '1'
   v2 = Voice(Note(2, (1, 4))*2)
   v2.name = '2'
   v3 = Voice(Note(4, (1, 4))*2)
   v3.name = '3'
   t1 = Staff([v1, v2, v3])
   t1.parallel = True
   t1.name = 'staff1'
   t2 = clone.fracture([t1])[0]
   t2.parallel = True
   t2.name = 'staff2'
   t3 = clone.fracture([t1])[0]
   t3.parallel = True
   t3.name = 'staff3'
   s1 = StaffGroup([t1, t2, t3])
   s1.name = 'sg'
   s2 = clone.fracture([s1])[0]
   s2.name = 'sg'
   s = Container([s1, s2])

   fuse.containers_by_reference(s)
   assert len(s) == 1
   assert s.format == '{\n\t\\context StaffGroup = "sg" <<\n\t\t\\context Staff = "staff1" <<\n\t\t\t\\context Voice = "1" {\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t}\n\t\t\t\\context Voice = "2" {\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t}\n\t\t\t\\context Voice = "3" {\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t}\n\t\t>>\n\t\t\\context Staff = "staff2" <<\n\t\t\t\\context Voice = "1" {\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t}\n\t\t\t\\context Voice = "2" {\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t}\n\t\t\t\\context Voice = "3" {\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t}\n\t\t>>\n\t\t\\context Staff = "staff3" <<\n\t\t\t\\context Voice = "1" {\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t}\n\t\t\t\\context Voice = "2" {\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t\td\'4\n\t\t\t}\n\t\t\t\\context Voice = "3" {\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t\te\'4\n\t\t\t}\n\t\t>>\n\t>>\n}'
 
   r'''
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

def test_fuse_containers_by_reference_10( ):
   '''Fuse nested parallel structures in sequence.'''

   v1a = Voice(Note(0, (1,4))*2)
   v1a.name = 'voiceOne'
   v1b = Voice(Note(0, (1,4))*2)
   v1b.name = 'voiceOne'
   v2a = Voice(Note(12, (1,4))*2)
   v2a.name = 'voiceTwo'
   v2b = Voice(Note(12, (1,4))*2)
   v2b.name = 'voiceTwo'
   s1 = Staff([v1a, v1b])
   s1.name ='staffOne'
   s2 = Staff([v2a, v2b])
   s2.name ='staffTwo'

   sg1 = StaffGroup([s1, s2])
   sg1.name ='groupOne'
   sg2 = clone.fracture([sg1])[0]
   sg2.name ='groupTwo'
   sg_g = StaffGroup([sg1, sg2])
   sg_g.name = 'topGroup'
   seq = fuse.containers_by_reference([sg_g, clone.fracture([sg_g])[0]])

   assert seq.format == '\\context StaffGroup = "topGroup" <<\n\t\\context StaffGroup = "groupOne" <<\n\t\t\\context Staff = "staffOne" {\n\t\t\t\\context Voice = "voiceOne" {\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t}\n\t\t}\n\t\t\\context Staff = "staffTwo" {\n\t\t\t\\context Voice = "voiceTwo" {\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t}\n\t\t}\n\t>>\n\t\\context StaffGroup = "groupTwo" <<\n\t\t\\context Staff = "staffOne" {\n\t\t\t\\context Voice = "voiceOne" {\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t\tc\'4\n\t\t\t}\n\t\t}\n\t\t\\context Staff = "staffTwo" {\n\t\t\t\\context Voice = "voiceTwo" {\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t\tc\'\'4\n\t\t\t}\n\t\t}\n\t>>\n>>'

   r'''
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
