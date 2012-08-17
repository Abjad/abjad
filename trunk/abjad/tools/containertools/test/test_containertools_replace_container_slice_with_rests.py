from abjad import *


#def test_containertools_replace_container_slice_with_rests_01():
#
#    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8")
#    containertools.replace_container_slice_with_rests(staff, stop=5, big_endian=True)
#
#    r'''
#    \new Staff {
#        r2
#        r8
#        a'8
#    }
#    '''
#
#    assert staff.lilypond_format == "\\new Staff {\n\tr2\n\tr8\n\ta'8\n}"
#
#
#def test_containertools_replace_container_slice_with_rests_02():
#
#    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8")
#    containertools.replace_container_slice_with_rests(staff, start=-5, big_endian=True)
#
#    r'''
#    \new Staff {
#        c'8
#        r2
#        r8
#    }
#    '''
#
#    assert staff.lilypond_format == "\\new Staff {\n\tc'8\n\tr2\n\tr8\n}"


def test_containertools_replace_container_slice_with_rests_03():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8")
    containertools.replace_container_slice_with_rests(staff, stop=5, big_endian=False)

    r'''
    \new Staff {
        r8
        r2
        a'8
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\tr8\n\tr2\n\ta'8\n}"


def test_containertools_replace_container_slice_with_rests_04():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8")
    containertools.replace_container_slice_with_rests(staff, start=-5, big_endian=False)

    r'''
    \new Staff {
        c'8
        r8
        r2
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\tc'8\n\tr8\n\tr2\n}"
