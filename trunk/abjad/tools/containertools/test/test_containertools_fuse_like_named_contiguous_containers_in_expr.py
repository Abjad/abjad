from abjad import *
import py.test


def test_containertools_fuse_like_named_contiguous_containers_in_expr_01():
    '''Do nothing on leaf.'''

    t = Note(1, (1, 4))
    result = containertools.fuse_like_named_contiguous_containers_in_expr(t)
    assert result is None
    assert isinstance(t, Note)


def test_containertools_fuse_like_named_contiguous_containers_in_expr_02():
    '''Do not fuse unnamed voices.'''

    t = Staff([Voice(notetools.make_repeated_notes(2)), Voice(notetools.make_repeated_notes(2))])
    result = containertools.fuse_like_named_contiguous_containers_in_expr(t)
    assert result is None


def test_containertools_fuse_like_named_contiguous_containers_in_expr_03():
    '''Do not fuse nonthreads.'''

    t = Staff([Voice(notetools.make_repeated_notes(2)), Voice(notetools.make_repeated_notes(2))])
    t[0].name = 'one'
    t[1].name = 'two'
    result = containertools.fuse_like_named_contiguous_containers_in_expr(t)
    assert result is None


def test_containertools_fuse_like_named_contiguous_containers_in_expr_04():
    '''Do not fuse tuplets.'''

    t = Voice([Tuplet(Fraction(2, 3), notetools.make_repeated_notes(3)),
        Tuplet(Fraction(2, 3), notetools.make_repeated_notes(3))])
    result = containertools.fuse_like_named_contiguous_containers_in_expr(t)
    assert result is None
    assert len(t) == 2


def test_containertools_fuse_like_named_contiguous_containers_in_expr_05():
    '''Fuse like-named staves.'''

    t = Staff(notetools.make_repeated_notes(4)) * 2
    t[0].name = t[1].name = 'staffOne'
    result = containertools.fuse_like_named_contiguous_containers_in_expr(t)
    assert isinstance(result, Staff)
    assert len(result) == 8


def test_containertools_fuse_like_named_contiguous_containers_in_expr_06():
    '''Fuse like-named staves but not differently named voices.'''

    t = Container(Staff([Voice(notetools.make_repeated_notes(4))]) * 2)
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

    result = containertools.fuse_like_named_contiguous_containers_in_expr(t)
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


def test_containertools_fuse_like_named_contiguous_containers_in_expr_07():
    '''Fuse orphan components.'''

    t = Voice(notetools.make_repeated_notes(4)) * 2
    t[0].name = t[1].name = 'voiceOne'
    result = containertools.fuse_like_named_contiguous_containers_in_expr(t)
    assert isinstance(result, Voice)
    assert len(result) == 8


# TODO this should work.
#def test_containertools_fuse_like_named_contiguous_containers_in_expr_08():
#   '''containertools.fuse_like_named_contiguous_containers_in_expr() can take a list of parented
#   Components.'''
#   t = Staff(Voice(notetools.make_repeated_notes(2)) * 2)
#   result = containertools.fuse_like_named_contiguous_containers_in_expr(t[:])
#   assert componenttools.is_well_formed_component(t)
#   assert len(t) == 1


# NESTED PARALLEL STRUCTURES #

def test_containertools_fuse_like_named_contiguous_containers_in_expr_09():
    '''Fuse parallel voices within parallel staves within parallel
    staff groups within a single container.
    '''

    v1 = Voice(Note("c'4")*2)
    v1.name = '1'
    v2 = Voice(Note(2, (1, 4))*2)
    v2.name = '2'
    v3 = Voice(Note(4, (1, 4))*2)
    v3.name = '3'
    t1 = Staff([v1, v2, v3])
    t1.is_parallel = True
    t1.name = 'staff1'
    t2 = componenttools.copy_components_and_fracture_crossing_spanners([t1])[0]
    t2.is_parallel = True
    t2.name = 'staff2'
    t3 = componenttools.copy_components_and_fracture_crossing_spanners([t1])[0]
    t3.is_parallel = True
    t3.name = 'staff3'
    s1 = scoretools.StaffGroup([t1, t2, t3])
    s1.name = 'sg'
    s2 = componenttools.copy_components_and_fracture_crossing_spanners([s1])[0]
    s2.name = 'sg'
    s = Container([s1, s2])

    containertools.fuse_like_named_contiguous_containers_in_expr(s)
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

def test_containertools_fuse_like_named_contiguous_containers_in_expr_10():
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

    sg1 = scoretools.StaffGroup([s1, s2])
    sg1.name ='groupOne'
    sg2 = componenttools.copy_components_and_fracture_crossing_spanners([sg1])[0]
    sg2.name ='groupTwo'
    sg_g = scoretools.StaffGroup([sg1, sg2])
    sg_g.name = 'topGroup'
    seq = containertools.fuse_like_named_contiguous_containers_in_expr([sg_g, componenttools.copy_components_and_fracture_crossing_spanners([sg_g])[0]])

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
