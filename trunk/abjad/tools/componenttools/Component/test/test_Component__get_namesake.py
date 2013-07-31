from abjad import *
import py.test


def test_Component__get_namesake_01():

    t = Staff("c'8 d'8 e'8 f'8")

    assert t[0]._get_namesake(0) is t[0]
    assert t[0]._get_namesake(1) is t[1]
    assert t[0]._get_namesake(2) is t[2]
    assert t[0]._get_namesake(3) is t[3]

    assert t[3]._get_namesake(0) is t[3]
    assert t[3]._get_namesake(-1) is t[2]
    assert t[3]._get_namesake(-2) is t[1]
    assert t[3]._get_namesake(-3) is t[0]


def test_Component__get_namesake_02():

    t = Staff("c'8 d'8 e'8 f'8")

    assert t[0]._get_namesake(99) is None


def test_Component__get_namesake_03():
    r'''Leaves within different anonymous parents have different
    parentage signatures and thus have no _next_namesake.
    '''

    t = Container(Voice(notetools.make_repeated_notes(2)) * 2)

    assert t.select_leaves()[0]._get_namesake(1) is t.select_leaves()[1]
    assert t.select_leaves()[1]._get_namesake(1) is None
    assert t.select_leaves()[2]._get_namesake(1) is t.select_leaves()[3]


def test_Component__get_namesake_04():
    r'''Anonymous containers with the same parentage structure have
    different parentage signatures and thus have no _next_namesake.
    '''

    t = Container(Voice(notetools.make_repeated_notes(2)) * 2)

    assert t[0]._get_namesake(1) is None


def test_Component__get_namesake_05():
    r'''Differently named containers have a different parentage signature
    and thus do not _next_namesake.
    '''

    t = Container(Voice(notetools.make_repeated_notes(2)) * 2)
    t[0].name = 'voice'

    assert t[0]._get_namesake(1) is None
    assert t.select_leaves()[0]._get_namesake(1) is t.select_leaves()[1]
    assert t.select_leaves()[1]._get_namesake(1) is None
    assert t.select_leaves()[2]._get_namesake(1) is t.select_leaves()[3]


def test_Component__get_namesake_06():
    r'''Calling _next_namesake on a named component when another component
    with the same type and name exists after the caller returns the first
    next namesake Component found.
    '''

    t = Container(Voice(notetools.make_repeated_notes(2)) * 2)
    t[0].name = 'voice'
    t[1].name = 'voice'

    assert t[0]._get_namesake(1) is t[1]
    assert t[1]._get_namesake(1) is None
    assert t.select_leaves()[1]._get_namesake(1) is t.select_leaves()[2]


def test_Component__get_namesake_07():
    r'''Components need not be strictly contiguous.
    '''

    t = Container(Voice(notetools.make_repeated_notes(2)) * 2)
    t[0].name = 'voice'
    t[1].name = 'voice'
    t.insert(1, Rest((1, 2)))

    assert t[0]._get_namesake(1) is t[2]
    assert t.select_leaves()[1]._get_namesake(1) is t.select_leaves()[3]


def test_Component__get_namesake_08():
    r'''Components need not thread (Staves don't thread).
    '''

    t = Container(Staff(notetools.make_repeated_notes(2)) * 2)
    t[0].name = 'staff'
    t[1].name = 'staff'

    assert t[0]._get_namesake(1) is t[1]
    assert t.select_leaves()[1]._get_namesake(1) is t.select_leaves()[2]


def test_Component__get_namesake_09():
    r'''_next_namesake works on parallel structures.
    '''

    a = Container(Voice(notetools.make_repeated_notes(2)) * 2)
    a[0].name = 'voiceOne'
    a[1].name = 'voiceTwo'
    a.is_parallel = True
    b = Container(Voice(notetools.make_repeated_notes(2)) * 2)
    b[0].name = 'voiceOne'
    b[1].name = 'voiceTwo'
    b.is_parallel = True
    t = Staff([a, b])

    r'''
    \new Staff {
        <<
            \context Voice = "voiceOne" {
                c'8
                c'8
            }
            \context Voice = "voiceTwo" {
                c'8
                c'8
            }
        >>
        <<
            \context Voice = "voiceOne" {
                c'8
                c'8
            }
            \context Voice = "voiceTwo" {
                c'8
                c'8
            }
        >>
    }
    '''

    assert a[0]._get_namesake(1) is b[0]
    assert a[1]._get_namesake(1) is b[1]
    assert a[0][1]._get_namesake(1) is b[0][0]
    assert a[1][1]._get_namesake(1) is b[1][0]
