from abjad import *
import py.test


def test_componenttools_get_nth_namesake_from_component_01():

    t = Staff("c'8 d'8 e'8 f'8")

    assert componenttools.get_nth_namesake_from_component(t[0], 0) is t[0]
    assert componenttools.get_nth_namesake_from_component(t[0], 1) is t[1]
    assert componenttools.get_nth_namesake_from_component(t[0], 2) is t[2]
    assert componenttools.get_nth_namesake_from_component(t[0], 3) is t[3]

    assert componenttools.get_nth_namesake_from_component(t[3], 0) is t[3]
    assert componenttools.get_nth_namesake_from_component(t[3], -1) is t[2]
    assert componenttools.get_nth_namesake_from_component(t[3], -2) is t[1]
    assert componenttools.get_nth_namesake_from_component(t[3], -3) is t[0]


def test_componenttools_get_nth_namesake_from_component_02():

    t = Staff("c'8 d'8 e'8 f'8")

    assert componenttools.get_nth_namesake_from_component(t[0], 99) is None


def test_componenttools_get_nth_namesake_from_component_03():
    '''Leaves within different anonymous parents have different
    parentage signatures and thus have no _next_namesake.
    '''

    t = Container(Voice(notetools.make_repeated_notes(2)) * 2)

    assert componenttools.get_nth_namesake_from_component(t.leaves[0], 1) is t.leaves[1]
    assert componenttools.get_nth_namesake_from_component(t.leaves[1], 1) is None
    assert componenttools.get_nth_namesake_from_component(t.leaves[2], 1) is t.leaves[3]


def test_componenttools_get_nth_namesake_from_component_04():
    '''Anonymous containers with the same parentage structure have
    different parentage signatures and thus have no _next_namesake.
    '''

    t = Container(Voice(notetools.make_repeated_notes(2)) * 2)

    assert componenttools.get_nth_namesake_from_component(t[0], 1) is None


def test_componenttools_get_nth_namesake_from_component_05():
    '''Differently named containers have a different parentage signature
    and thus do not _next_namesake.
    '''

    t = Container(Voice(notetools.make_repeated_notes(2)) * 2)
    t[0].name = 'voice'

    assert componenttools.get_nth_namesake_from_component(t[0], 1) is None
    assert componenttools.get_nth_namesake_from_component(t.leaves[0], 1) is t.leaves[1]
    assert componenttools.get_nth_namesake_from_component(t.leaves[1], 1) is None
    assert componenttools.get_nth_namesake_from_component(t.leaves[2], 1) is t.leaves[3]


def test_componenttools_get_nth_namesake_from_component_06():
    '''Calling _next_namesake on a named component when another component
    with the same type and name exists after the caller returns the first
    next namesake Component found.
    '''

    t = Container(Voice(notetools.make_repeated_notes(2)) * 2)
    t[0].name = 'voice'
    t[1].name = 'voice'

    assert componenttools.get_nth_namesake_from_component(t[0], 1) is t[1]
    assert componenttools.get_nth_namesake_from_component(t[1], 1) is None
    assert componenttools.get_nth_namesake_from_component(t.leaves[1], 1) is t.leaves[2]


def test_componenttools_get_nth_namesake_from_component_07():
    '''Components need not be strictly contiguous.
    '''

    t = Container(Voice(notetools.make_repeated_notes(2)) * 2)
    t[0].name = 'voice'
    t[1].name = 'voice'
    t.insert(1, Rest((1, 2)))

    assert componenttools.get_nth_namesake_from_component(t[0], 1) is t[2]
    assert componenttools.get_nth_namesake_from_component(t.leaves[1], 1) is t.leaves[3]


def test_componenttools_get_nth_namesake_from_component_08():
    '''Components need not thread (Staves don't thread).
    '''

    t = Container(Staff(notetools.make_repeated_notes(2)) * 2)
    t[0].name = 'staff'
    t[1].name = 'staff'

    assert componenttools.get_nth_namesake_from_component(t[0], 1) is t[1]
    assert componenttools.get_nth_namesake_from_component(t.leaves[1], 1) is t.leaves[2]


def test_componenttools_get_nth_namesake_from_component_09():
    '''_next_namesake works on parallel structures.
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

    assert componenttools.get_nth_namesake_from_component(a[0], 1) is b[0]
    assert componenttools.get_nth_namesake_from_component(a[1], 1) is b[1]
    assert componenttools.get_nth_namesake_from_component(a[0][1], 1) is b[0][0]
    assert componenttools.get_nth_namesake_from_component(a[1][1], 1) is b[1][0]
