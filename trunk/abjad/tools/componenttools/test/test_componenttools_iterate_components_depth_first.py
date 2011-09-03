from abjad import *
import py.test


# NOTE: all tests operate on the following expression #

t = Staff(notetools.make_repeated_notes(4))
t.insert(2, Container(Voice(notetools.make_repeated_notes(2)) * 2))
t[2].is_parallel = True
pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

r'''
\new Staff {
    c'8
    cs'8
    <<
        \new Voice {
            d'8
            ef'8
        }
        \new Voice {
            e'8
            f'8
        }
    >>
    fs'8
    g'8
}
'''


def test_componenttools_iterate_components_depth_first_01():
    '''
    Default depth-first search:
        * capped iteration returns no elements above self._client
        * unique returns each node at most once
        * no classes forbidden means all containers entered
    '''

    # LEFT-TO-RIGHT #

    g = componenttools.iterate_components_depth_first(t[2])

    assert g.next() is t[2]
    assert g.next() is t[2][0]
    assert g.next() is t[2][0][0]
    assert g.next() is t[2][0][1]
    assert g.next() is t[2][1]
    assert g.next() is t[2][1][0]
    assert g.next() is t[2][1][1]
    assert py.test.raises(StopIteration, 'g.next()')

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(d'8, ef'8)
    d'8
    ef'8
    Voice(e'8, f'8)
    e'8
    f'8
    '''

    # RIGHT-TO-LEFT #

    g = componenttools.iterate_components_depth_first(t[2], direction = 'right')

    assert g.next() is t[2]
    assert g.next() is t[2][1]
    assert g.next() is t[2][1][1]
    assert g.next() is t[2][1][0]
    assert g.next() is t[2][0]
    assert g.next() is t[2][0][1]
    assert g.next() is t[2][0][0]
    assert py.test.raises(StopIteration, 'g.next()')

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(e'8, f'8)
    f'8
    e'8
    Voice(d'8, ef'8)
    ef'8
    d'8
    '''


def test_componenttools_iterate_components_depth_first_02():
    '''Uncapped depth-first search: uncapped iteration returns
    all elements above self._client
    '''

    # LEFT-TO-RIGHT #

    g = componenttools.iterate_components_depth_first(t[2], capped = False)

    assert g.next() is t[2]
    assert g.next() is t[2][0]
    assert g.next() is t[2][0][0]
    assert g.next() is t[2][0][1]
    assert g.next() is t[2][1]
    assert g.next() is t[2][1][0]
    assert g.next() is t[2][1][1]
    assert g.next() is t
    assert g.next() is t[3]
    assert g.next() is t[4]
    assert py.test.raises(StopIteration, 'g.next()')

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(d'8, ef'8)
    d'8
    ef'8
    Voice(e'8, f'8)
    e'8
    f'8
    Staff{5}
    fs'8
    g'8
    '''

    # RIGHT-TO-LEFT #

    g = componenttools.iterate_components_depth_first(t[2], capped = False, direction = 'right')

    assert g.next() is t[2]
    assert g.next() is t[2][1]
    assert g.next() is t[2][1][1]
    assert g.next() is t[2][1][0]
    assert g.next() is t[2][0]
    assert g.next() is t[2][0][1]
    assert g.next() is t[2][0][0]
    assert g.next() is t
    assert g.next() is t[1]
    assert g.next() is t[0]
    assert py.test.raises(StopIteration, 'g.next()')

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(e'8, f'8)
    f'8
    e'8
    Voice(d'8, ef'8)
    ef'8
    d'8
    Staff{5}
    cs'8
    c'8
    '''


def test_componenttools_iterate_components_depth_first_03():
    '''Duplicates-allowed depth-first search: nodes yield every time they are traversed.
    '''

    # LEFT-TO-RIGHT #

    g = componenttools.iterate_components_depth_first(t[2], unique = False)

    assert g.next() is t[2]
    assert g.next() is t[2][0]
    assert g.next() is t[2][0][0]
    assert g.next() is t[2][0]
    assert g.next() is t[2][0][1]
    assert g.next() is t[2][0]
    assert g.next() is t[2]
    assert g.next() is t[2][1]
    assert g.next() is t[2][1][0]
    assert g.next() is t[2][1]
    assert g.next() is t[2][1][1]
    assert g.next() is t[2][1]
    assert g.next() is t[2]
    assert py.test.raises(StopIteration, 'g.next()')

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(d'8, ef'8)
    d'8
    Voice(d'8, ef'8)
    ef'8
    Voice(d'8, ef'8)
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(e'8, f'8)
    e'8
    Voice(e'8, f'8)
    f'8
    Voice(e'8, f'8)
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    '''

    # RIGHT-TO-LEFT #

    g = componenttools.iterate_components_depth_first(t[2], unique = False, direction = 'right')

    assert g.next() is t[2]
    assert g.next() is t[2][1]
    assert g.next() is t[2][1][1]
    assert g.next() is t[2][1]
    assert g.next() is t[2][1][0]
    assert g.next() is t[2][1]
    assert g.next() is t[2]
    assert g.next() is t[2][0]
    assert g.next() is t[2][0][1]
    assert g.next() is t[2][0]
    assert g.next() is t[2][0][0]
    assert g.next() is t[2][0]
    assert g.next() is t[2]
    assert py.test.raises(StopIteration, 'g.next()')

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(e'8, f'8)
    f'8
    Voice(e'8, f'8)
    e'8
    Voice(e'8, f'8)
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(d'8, ef'8)
    ef'8
    Voice(d'8, ef'8)
    d'8
    Voice(d'8, ef'8)
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    '''


def test_componenttools_iterate_components_depth_first_04():
    '''Restricted depth-first search: iteration will yield -- but will not
    enter -- forbidden classes.
    '''

    # LEFT-TO-RIGHT #

    g = componenttools.iterate_components_depth_first(t, forbid = 'parallel')

    assert g.next() is t
    assert g.next() is t[0]
    assert g.next() is t[1]
    assert g.next() is t[2]
    assert g.next() is t[3]
    assert g.next() is t[4]
    assert py.test.raises(StopIteration, 'g.next()')

    r'''
    Staff{5}
    c'8
    cs'8
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    fs'8
    g'8
    '''

    # RIGHT-TO-LEFT #

    g = componenttools.iterate_components_depth_first(t, forbid = 'parallel', direction = 'right')

    assert g.next() is t
    assert g.next() is t[4]
    assert g.next() is t[3]
    assert g.next() is t[2]
    assert g.next() is t[1]
    assert g.next() is t[0]
    assert py.test.raises(StopIteration, 'g.next()')

    r'''
    Staff{5}
    g'8
    fs'8
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    cs'8
    c'8
    '''


def test_componenttools_iterate_components_depth_first_05():
    '''Uncapped depth-first search with duplicates allowed.
    '''

    # LEFT-TO-RIGHT #

    g = componenttools.iterate_components_depth_first(t[2], capped = False, unique = False)

    assert g.next() is t[2]
    assert g.next() is t[2][0]
    assert g.next() is t[2][0][0]
    assert g.next() is t[2][0]
    assert g.next() is t[2][0][1]
    assert g.next() is t[2][0]
    assert g.next() is t[2]
    assert g.next() is t[2][1]
    assert g.next() is t[2][1][0]
    assert g.next() is t[2][1]
    assert g.next() is t[2][1][1]
    assert g.next() is t[2][1]
    assert g.next() is t[2]
    assert g.next() is t
    assert g.next() is t[3]
    assert g.next() is t
    assert g.next() is t[4]
    assert g.next() is t
    assert py.test.raises(StopIteration, 'g.next()')

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(d'8, ef'8)
    d'8
    Voice(d'8, ef'8)
    ef'8
    Voice(d'8, ef'8)
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(e'8, f'8)
    e'8
    Voice(e'8, f'8)
    f'8
    Voice(e'8, f'8)
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Staff{5}
    fs'8
    Staff{5}
    g'8
    Staff{5}
    '''

    # RIGHT-TO-LEFT #

    g = componenttools.iterate_components_depth_first(
        t[2], capped = False, unique = False, direction = 'right')

    assert g.next() is t[2]
    assert g.next() is t[2][1]
    assert g.next() is t[2][1][1]
    assert g.next() is t[2][1]
    assert g.next() is t[2][1][0]
    assert g.next() is t[2][1]
    assert g.next() is t[2]
    assert g.next() is t[2][0]
    assert g.next() is t[2][0][1]
    assert g.next() is t[2][0]
    assert g.next() is t[2][0][0]
    assert g.next() is t[2][0]
    assert g.next() is t[2]
    assert g.next() is t
    assert g.next() is t[1]
    assert g.next() is t
    assert g.next() is t[0]
    assert g.next() is t
    assert py.test.raises(StopIteration, 'g.next()')

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(e'8, f'8)
    f'8
    Voice(e'8, f'8)
    e'8
    Voice(e'8, f'8)
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(d'8, ef'8)
    ef'8
    Voice(d'8, ef'8)
    d'8
    Voice(d'8, ef'8)
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Staff{5}
    cs'8
    Staff{5}
    c'8
    Staff{5}
    '''


def test_componenttools_iterate_components_depth_first_06():
    '''Uncapped and restricted depth-first search.
    '''

    # LEFT-TO-RIGHT #

    g = componenttools.iterate_components_depth_first(t[2], capped = False, forbid = 'parallel')

    assert g.next() is t[2]
    assert g.next() is t
    assert g.next() is t[3]
    assert g.next() is t[4]

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Staff{5}
    fs'8
    g'8
    '''

    # RIGHT-TO-LEFT #

    g = componenttools.iterate_components_depth_first(
        t[2], capped = False, forbid = 'parallel', direction = 'right')

    assert g.next() is t[2]
    assert g.next() is t
    assert g.next() is t[1]
    assert g.next() is t[0]

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Staff{5}
    cs'8
    c'8
    '''


def test_componenttools_iterate_components_depth_first_07():
    '''Restricted depth-first search with duplicates allowed.
    '''

    # LEFT-TO-RIGHT

    g = componenttools.iterate_components_depth_first(t, forbid = 'parallel', unique = False)

    assert g.next() is t
    assert g.next() is t[0]
    assert g.next() is t
    assert g.next() is t[1]
    assert g.next() is t
    assert g.next() is t[2]
    assert g.next() is t
    assert g.next() is t[3]
    assert g.next() is t
    assert g.next() is t[4]
    assert g.next() is t
    assert py.test.raises(StopIteration, 'g.next()')

    r'''
    Staff{5}
    c'8
    Staff{5}
    cs'8
    Staff{5}
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Staff{5}
    fs'8
    Staff{5}
    g'8
    Staff{5}
    '''

    # RIGHT-TO-LEFT #

    g = componenttools.iterate_components_depth_first(
        t, forbid = 'parallel', unique = False, direction = 'right')

    assert g.next() is t
    assert g.next() is t[4]
    assert g.next() is t
    assert g.next() is t[3]
    assert g.next() is t
    assert g.next() is t[2]
    assert g.next() is t
    assert g.next() is t[1]
    assert g.next() is t
    assert g.next() is t[0]
    assert g.next() is t
    assert py.test.raises(StopIteration, 'g.next()')

    r'''
    Staff{5}
    g'8
    Staff{5}
    fs'8
    Staff{5}
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Staff{5}
    cs'8
    Staff{5}
    c'8
    Staff{5}
    '''


def test_componenttools_iterate_components_depth_first_08():
    '''Uncapped but restricted depth-first serach with duplicates allowed.
    '''

    # LEFT-TO-RIGHT #

    g = componenttools.iterate_components_depth_first(
        t[2], capped = False, forbid = 'parallel', unique = False)

    assert g.next() is t[2]
    assert g.next() is t
    assert g.next() is t[3]
    assert g.next() is t
    assert g.next() is t[4]
    assert g.next() is t
    assert py.test.raises(StopIteration, 'g.next()')

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Staff{5}
    fs'8
    Staff{5}
    g'8
    Staff{5}
    '''

    # RIGHT-TO-LEFT #

    g = componenttools.iterate_components_depth_first(
        t[2], capped = False, forbid = 'parallel', unique = False, direction = 'right')

    assert g.next() is t[2]
    assert g.next() is t
    assert g.next() is t[1]
    assert g.next() is t
    assert g.next() is t[0]
    assert g.next() is t
    assert py.test.raises(StopIteration, 'g.next()')

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Staff{5}
    cs'8
    Staff{5}
    c'8
    Staff{5}
    '''
