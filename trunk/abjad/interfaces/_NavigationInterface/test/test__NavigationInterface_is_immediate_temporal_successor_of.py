from abjad import *
import py.test


def test__NavigationInterface_is_immediate_temporal_successor_of_01( ):
    '''The second of two leaves in the same voice is
        the immediate temporal follower of the first.'''

    t = Voice([Note(i, (1, 8)) for i in range(4)])

    assert t[0]._navigator._is_immediate_temporal_successor_of(t[1])
    assert t[1]._navigator._is_immediate_temporal_successor_of(t[2])
    assert t[2]._navigator._is_immediate_temporal_successor_of(t[3])

    r'''
    \new Voice {
        c'8
        cs'8
        d'8
        ef'8
    }
    '''


def test__NavigationInterface_is_immediate_temporal_successor_of_02( ):
    '''The second of two leaves in the same staff is
        the immediate temporal follower of the first.'''

    t = Staff([Note(i, (1, 8)) for i in range(4)])

    assert t[0]._navigator._is_immediate_temporal_successor_of(t[1])
    assert t[1]._navigator._is_immediate_temporal_successor_of(t[2])
    assert t[2]._navigator._is_immediate_temporal_successor_of(t[3])

    r'''
    \new Staff {
        c'8
        cs'8
        d'8
        ef'8
    }
    '''


def test__NavigationInterface_is_immediate_temporal_successor_of_03( ):
    '''The second of two leaves in the same sequential is
        the immediate temporal follower of the first.'''

    t = Staff([Note(i, (1, 8)) for i in range(4)])

    assert t[0]._navigator._is_immediate_temporal_successor_of(t[1])
    assert t[1]._navigator._is_immediate_temporal_successor_of(t[2])
    assert t[2]._navigator._is_immediate_temporal_successor_of(t[3])

    r'''
    {
        c'8
        cs'8
        d'8
        ef'8
    }
    '''


# NONSTRUCTURAL in new parallel --> context model.
#def test__NavigationInterface_is_immediate_temporal_successor_of_04( ):
#   '''None of the leaves in the same parallel follow
#      any of the others temporally.'''
#
#   t = Container([Note(i, (1, 8)) for i in range(4)])
#   t.is_parallel = True
#
#   assert not t[0]._navigator._is_immediate_temporal_successor_of(t[1])
#   assert not t[1]._navigator._is_immediate_temporal_successor_of(t[2])
#   assert not t[2]._navigator._is_immediate_temporal_successor_of(t[3])
#
#   r'''<<
#      c'8
#      cs'8
#      d'8
#      ef'8
#   >>'''


def test__NavigationInterface_is_immediate_temporal_successor_of_05( ):
    '''The second of two leaves in the same tuplet is
        the immediate temporal follower of the first.'''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), [Note(i, (1, 8)) for i in range(3)])

    assert t[0]._navigator._is_immediate_temporal_successor_of(t[1])
    assert t[1]._navigator._is_immediate_temporal_successor_of(t[2])

    r'''
    \times 2/3 {
        c'8
        cs'8
        d'8
    }
    '''


def test__NavigationInterface_is_immediate_temporal_successor_of_06( ):
    '''The second sequential and the first note of the second sequential
        both temporally follow the first sequential and the last
        note of the first sequential immediately.'''

    s1 = Container([Note(i, (1, 8)) for i in range(4)])
    s2 = Container([Note(i, (1, 8)) for i in range(4, 8)])
    t = Voice([s1, s2])

    assert t[0]._navigator._is_immediate_temporal_successor_of(t[1])
    assert t[0]._navigator._is_immediate_temporal_successor_of(t[1][0])
    assert t[0][-1]._navigator._is_immediate_temporal_successor_of(t[1])
    assert t[0][-1]._navigator._is_immediate_temporal_successor_of(t[1][0])

    r'''
    \new Voice {
        {
            c'8
            cs'8
            d'8
            ef'8
        }
        {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''


def test__NavigationInterface_is_immediate_temporal_successor_of_07( ):
    '''The second tuplet and the first note of the second tuplet
        both temporally follow the first tuplet and the last
        note of the first tuplet immediately.'''

    t1 = tuplettools.FixedDurationTuplet(Duration(2, 8), [Note(i, (1, 8)) for i in range(3)])
    t2 = tuplettools.FixedDurationTuplet(Duration(2, 8), [Note(i, (1, 8)) for i in range(3, 6)])
    t = Voice([t1, t2])

    assert t[0]._navigator._is_immediate_temporal_successor_of(t[1])
    assert t[0]._navigator._is_immediate_temporal_successor_of(t[1][0])
    assert t[0][-1]._navigator._is_immediate_temporal_successor_of(t[1])
    assert t[0][-1]._navigator._is_immediate_temporal_successor_of(t[1][0])

    r'''
    \new Voice {
        \times 2/3 {
            c'8
            cs'8
            d'8
        }
        \times 2/3 {
            ef'8
            e'8
            f'8
        }
    }
    '''


def test__NavigationInterface_is_immediate_temporal_successor_of_08( ):
    '''The second (anonymous) voice and the first note of the
        second (anonymous) voice both temporally follow the
        first (anonymous) voice and the last note of the
        first (anonymous) voice immediately.'''

    v1 = Voice([Note(i, (1, 8)) for i in range(4)])
    v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
    t = Staff([v1, v2])

    assert t[0]._navigator._is_immediate_temporal_successor_of(t[1])
    assert t[0]._navigator._is_immediate_temporal_successor_of(t[1][0])
    assert t[0][-1]._navigator._is_immediate_temporal_successor_of(t[1])
    assert t[0][-1]._navigator._is_immediate_temporal_successor_of(t[1][0])

    r'''
    \new Staff {
        \new Voice {
            c'8
            cs'8
            d'8
            ef'8
        }
        \new Voice {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''


def test__NavigationInterface_is_immediate_temporal_successor_of_09( ):
    '''The second (like-named) voice and the first note of the
        second (like-named) voice both temporally follow the
        first (like-named) voice and the last note of the
        first (like-named) voice immediately.'''

    v1 = Voice([Note(i, (1, 8)) for i in range(4)])
    v1.name = 'foo'
    v2 = Voice([Note(i, (1, 8)) for i in range(4, 88)])
    v2.name = 'foo'
    t = Staff([v1, v2])

    assert t[0]._navigator._is_immediate_temporal_successor_of(t[1])
    assert t[0]._navigator._is_immediate_temporal_successor_of(t[1][0])
    assert t[0][-1]._navigator._is_immediate_temporal_successor_of(t[1])

    r'''
    \new Staff {
        \context Voice = "foo" {
            c'8
            cs'8
            d'8
            ef'8
        }
        \context Voice = "foo" {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''


def test__NavigationInterface_is_immediate_temporal_successor_of_10( ):
    '''The second (differently named) voice and the first note of the
        second (differently named) voice both temporally follow the
        first (differently named) voice and the last note of the
        first (differently named) voice immediately.'''

    v1 = Voice([Note(i, (1, 8)) for i in range(4)])
    v1.name = 'foo'
    v2 = Voice([Note(i, (1, 8)) for i in range(4, 88)])
    v2.name = 'bar'
    t = Staff([v1, v2])

    assert t[0]._navigator._is_immediate_temporal_successor_of(t[1])
    assert t[0]._navigator._is_immediate_temporal_successor_of(t[1][0])
    assert t[0][-1]._navigator._is_immediate_temporal_successor_of(t[1])

    r'''
    \new Staff {
        \context Voice = "foo" {
            c'8
            cs'8
            d'8
            ef'8
        }
        \context Voice = "bar" {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''


def test__NavigationInterface_is_immediate_temporal_successor_of_11( ):
    '''Each of ...
        * the first (anonymous) staff
        * the first (anonymous) voice
        * the last note in the first (anonymous) voice
    ... is followed in immediate temporal order by each of ...
        * the second (anonymous) staff
        * the second (anonymous) voice
        * the first note in the second (anonymous) voice.'''

    v1 = Voice([Note(i, (1, 8)) for i in range(4)])
    v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
    s1 = Staff([v1])
    s2 = Staff([v2])
    seq = Container([s1, s2])

    assert seq[0]._navigator._is_immediate_temporal_successor_of(seq[1])
    assert seq[0]._navigator._is_immediate_temporal_successor_of(seq[1][0])
    assert seq[0]._navigator._is_immediate_temporal_successor_of(seq[1][0][0])

    assert seq[0][0]._navigator._is_immediate_temporal_successor_of(seq[1])
    assert seq[0][0]._navigator._is_immediate_temporal_successor_of(seq[1][0])
    assert seq[0][0]._navigator._is_immediate_temporal_successor_of(seq[1][0][0])

    assert seq[0][0][-1]._navigator._is_immediate_temporal_successor_of(seq[1])
    assert seq[0][0][-1]._navigator._is_immediate_temporal_successor_of(seq[1][0])
    assert seq[0][0][-1]._navigator._is_immediate_temporal_successor_of(seq[1][0][0])

    r'''
    {
        \new Staff {
            \new Voice {
                c'8
                cs'8
                d'8
                ef'8
            }
        }
        \new Staff {
            \new Voice {
                e'8
                f'8
                fs'8
                g'8
            }
        }
    }
    '''


def test__NavigationInterface_is_immediate_temporal_successor_of_12( ):
    '''Everything at the beginning of the second staff temporally
        follows everything at the end of the first staff immediately.'''

    vl1 = Voice([Note(i, (1, 8)) for i in range(4)])
    vl2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
    vh1 = Voice([Note(i, (1, 8)) for i in range(12, 16)])
    vh2 = Voice([Note(i, (1, 8)) for i in range(16, 20)])
    s1 = Staff([vh1, vl1])
    s1.is_parallel = True
    s2 = Staff([vl2, vh2])
    s2.is_parallel = True
    seq = Container([s1, s2])

    assert seq[0]._navigator._is_immediate_temporal_successor_of(seq[1])
    assert seq[0]._navigator._is_immediate_temporal_successor_of(seq[1][0])
    assert seq[0]._navigator._is_immediate_temporal_successor_of(seq[1][0][0])
    assert seq[0]._navigator._is_immediate_temporal_successor_of(seq[1][1])
    assert seq[0]._navigator._is_immediate_temporal_successor_of(seq[1][1][0])

    assert seq[0][0]._navigator._is_immediate_temporal_successor_of(seq[1])
    assert seq[0][0]._navigator._is_immediate_temporal_successor_of(seq[1][0])
    assert seq[0][0]._navigator._is_immediate_temporal_successor_of(seq[1][0][0])
    assert seq[0][0]._navigator._is_immediate_temporal_successor_of(seq[1][1])
    assert seq[0][0]._navigator._is_immediate_temporal_successor_of(seq[1][1][0])

    assert seq[0][0][-1]._navigator._is_immediate_temporal_successor_of(seq[1])
    assert seq[0][0][-1]._navigator._is_immediate_temporal_successor_of(seq[1][0])
    assert seq[0][0][-1]._navigator._is_immediate_temporal_successor_of(seq[1][0][0])
    assert seq[0][0][-1]._navigator._is_immediate_temporal_successor_of(seq[1][1])
    assert seq[0][0][-1]._navigator._is_immediate_temporal_successor_of(seq[1][1][0])

    assert seq[0][1]._navigator._is_immediate_temporal_successor_of(seq[1])
    assert seq[0][1]._navigator._is_immediate_temporal_successor_of(seq[1][0])
    assert seq[0][1]._navigator._is_immediate_temporal_successor_of(seq[1][0][0])
    assert seq[0][1]._navigator._is_immediate_temporal_successor_of(seq[1][1])
    assert seq[0][1]._navigator._is_immediate_temporal_successor_of(seq[1][1][0])

    assert seq[0][1][-1]._navigator._is_immediate_temporal_successor_of(seq[1])
    assert seq[0][1][-1]._navigator._is_immediate_temporal_successor_of(seq[1][0])
    assert seq[0][1][-1]._navigator._is_immediate_temporal_successor_of(seq[1][0][0])
    assert seq[0][1][-1]._navigator._is_immediate_temporal_successor_of(seq[1][1])
    assert seq[0][1][-1]._navigator._is_immediate_temporal_successor_of(seq[1][1][0])

    r'''
    {
        \new Staff <<
            \new Voice {
                c''8
                cs''8
                d''8
                ef''8
            }
            \new Voice {
                c'8
                cs'8
                d'8
                ef'8
            }
        >>
        \new Staff <<
            \new Voice {
                e'8
                f'8
                fs'8
                g'8
            }
            \new Voice {
                e''8
                f''8
                fs''8
                g''8
            }
        >>
    }
    '''


def test__NavigationInterface_is_immediate_temporal_successor_of_13( ):
    '''Everything at the beginning of the second sequential temporally
        follows everything at the end of the first sequential immediately.'''

    s1 = Container([Note(i, (1, 8)) for i in range(4)])
    s1 = Container([s1])
    s2 = Container([Note(i, (1, 8)) for i in range(4, 8)])
    s2 = Container([s2])
    t = Voice([s1, s2])

    assert t[0]._navigator._is_immediate_temporal_successor_of(t[1])
    assert t[0]._navigator._is_immediate_temporal_successor_of(t[1][0])
    assert t[0]._navigator._is_immediate_temporal_successor_of(t[1][0][0])

    assert t[0][0]._navigator._is_immediate_temporal_successor_of(t[1])
    assert t[0][0]._navigator._is_immediate_temporal_successor_of(t[1][0])
    assert t[0][0]._navigator._is_immediate_temporal_successor_of(t[1][0][0])

    assert t[0][0][-1]._navigator._is_immediate_temporal_successor_of(t[1])
    assert t[0][0][-1]._navigator._is_immediate_temporal_successor_of(t[1][0])
    assert t[0][0][-1]._navigator._is_immediate_temporal_successor_of(t[1][0][0])

    r'''
    \new Voice {
        {
            {
                c'8
                cs'8
                d'8
                ef'8
            }
        }
        {
            {
                e'8
                f'8
                fs'8
                g'8
            }
        }
    }
    '''
