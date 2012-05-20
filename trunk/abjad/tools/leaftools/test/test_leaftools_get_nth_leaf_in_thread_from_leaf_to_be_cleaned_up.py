from abjad import *
import py


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_01():
    '''Voice.
    '''

    t = Voice([Note(i, (1,8)) for i in range(4)])

    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[0], 1) is t[1]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[1], 1) is t[2]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[2], 1) is t[3]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[3], 1) is None

    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[0], -1) is None
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[1], -1) is t[0]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[2], -1) is t[1]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[3], -1) is t[2]

    r'''
    \new Voice {
        c'8
        cs'8
        d'8
        ef'8
    }
    '''


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_02():
    '''Staff.
    '''

    t = Staff([Note(i, (1,8)) for i in range(4)])

    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[0], 1) is t[1]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[1], 1) is t[2]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[2], 1) is t[3]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[3], 1) is None

    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[0], -1) is None
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[1], -1) is t[0]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[2], -1) is t[1]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[3], -1) is t[2]

    r'''
    \new Staff {
        c'8
        cs'8
        d'8
        ef'8
    }
    '''


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_03():
    '''Container.
    '''

    t = Container([Note(i, (1,8)) for i in range(4)])

    r'''
    {
        c'8
        cs'8
        d'8
        ef'8
    }
    '''

    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[0], 1) is t[1]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[1], 1) is t[2]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[2], 1) is t[3]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[3], 1) is None

    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[0], -1) is None
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[1], -1) is t[0]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[2], -1) is t[1]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[3], -1) is t[2]


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_04():
    '''Fixed-duration tuplet.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2,8), [Note(i, (1,8)) for i in range(3)])

    r'''
    \times 2/3 {
        c'8
        cs'8
        d'8
    }
    '''

    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[0], 1) is t[1]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[1], 1) is t[2]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[2], 1) is None

    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[0], -1) is None
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[1], -1) is t[0]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t[2], -1) is t[1]


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_05():
    '''Contiguous containers inside a voice.
    '''

    s1 = Container([Note(i, (1,8)) for i in range(4)])
    s2 = Container([Note(i, (1,8)) for i in range(4,8)])
    t = Voice([s1, s2])

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

    assert leaftools.get_nth_leaf_in_thread_from_leaf(s1[0], 1) is s1[1]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(s1[1], 1) is s1[2]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(s1[2], 1) is s1[3]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(s1[3], 1) is s2[0]

    assert leaftools.get_nth_leaf_in_thread_from_leaf(s1[1], -1) is s1[0]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(s1[2], -1) is s1[1]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(s1[3], -1) is s1[2]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(s2[0], -1) is s1[3]


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_06():
    '''Tuplets inside a voice.
    '''

    t1 = tuplettools.FixedDurationTuplet(Duration(2,8), [Note(i, (1,8)) for i in range(3)])
    t2 = tuplettools.FixedDurationTuplet(Duration(2,8), [Note(i, (1,8)) for i in range(3,6)])
    t = Voice([t1, t2])

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

    assert leaftools.get_nth_leaf_in_thread_from_leaf(t1[0], 1) is t1[1]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t1[1], 1) is t1[2]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t1[2], 1) is t2[0]

    assert leaftools.get_nth_leaf_in_thread_from_leaf(t1[1], -1) is t1[0]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t1[2], -1) is t1[1]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(t2[0], -1) is t1[2]


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_07():
    '''Does not continue across contiguous anonymous voices inside a staff.
    '''

    v1 = Voice([Note(i, (1,8)) for i in range(4)])
    v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
    t = Staff([v1, v2])

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

    assert leaftools.get_nth_leaf_in_thread_from_leaf(v1[3], 1) is None
    assert leaftools.get_nth_leaf_in_thread_from_leaf(v2[0], -1) is None


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_08():
    '''Does cross contiguous equally named voices inside a staff.
    '''

    v1 = Voice([Note(i, (1,8)) for i in range(4)])
    v1.name = 'myvoice'
    v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
    v2.name = 'myvoice'
    t = Staff([v1, v2])

    r'''
    \new Staff {
        \context Voice = "myvoice" {
            c'8
            cs'8
            d'8
            ef'8
        }
        \context Voice = "myvoice" {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''

    assert leaftools.get_nth_leaf_in_thread_from_leaf(v1[0], 1) is v1[1]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(v1[1], 1) is v1[2]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(v1[2], 1) is v1[3]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(v1[3], 1) is v2[0]

    assert leaftools.get_nth_leaf_in_thread_from_leaf(v1[1], -1) is v1[0]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(v1[2], -1) is v1[1]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(v1[3], -1) is v1[2]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(v2[0], -1) is v1[3]


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_09():
    '''Does not connect through contiguous unequally named voices.
    '''

    v1 = Voice([Note(i, (1,8)) for i in range(4)])
    v1.name = 'yourvoice'
    v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
    v2.name = 'myvoice'
    t = Staff([v1, v2])

    r'''
    \new Staff {
        \context Voice = "yourvoice" {
            c'8
            cs'8
            d'8
            ef'8
        }
        \context Voice = "myvoice" {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''

    assert leaftools.get_nth_leaf_in_thread_from_leaf(v1[0], 1) is v1[1]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(v1[1], 1) is v1[2]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(v1[2], 1) is v1[3]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(v1[3], 1) is None

    v2.name = None
    assert leaftools.get_nth_leaf_in_thread_from_leaf(v1[3], 1) is None

    assert leaftools.get_nth_leaf_in_thread_from_leaf(v2[1], -1) is v2[0]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(v2[2], -1) is v2[1]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(v2[3], -1) is v2[2]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(v2[0], -1) is None


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_10():
    '''Does not connect through unequally named staves.
    '''

    v1 = Voice([Note(i, (1,8)) for i in range(4)])
    v1.name = 'low'
    v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
    v2.name = 'low'

    s1 = Staff([v1])
    s1.name = 'mystaff'
    s2 = Staff([v2])
    s2.name = 'mystaff'

    seq = Container([s1, s2])

    r'''
    {
        \context Staff = "mystaff" {
            \context Voice = "low" {
                c'8
                cs'8
                d'8
                ef'8
            }
        }
        \context Staff = "mystaff" {
            \context Voice = "low" {
                e'8
                f'8
                fs'8
                g'8
            }
        }
    }
    '''

    assert not leaftools.get_nth_leaf_in_thread_from_leaf(v1[3], 1) is v2[0]
    assert not leaftools.get_nth_leaf_in_thread_from_leaf(v2[0], -1) is v1[3]


py.test.skip('modernize from here to end of file.')
def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_11():
    '''Does not connect through equally named staves.
    '''

    vl1 = Voice([Note(i, (1,8)) for i in range(4)])
    vl1.name = 'low'
    vl2 = Voice([Note(i, (1,8)) for i in range(4,8)])
    vl2.name = 'low'
    vh1 = Voice([Note(i, (1,8)) for i in range(12,16)])
    vh1.name = 'high'
    vh2 = Voice([Note(i, (1,8)) for i in range(16,20)])
    vh2.name = 'high'

    s1 = Staff([vh1, vl1])
    s1.name = 'mystaff'
    s1.is_parallel = True
    s2 = Staff([vl2, vh2])
    s2.name = 'mystaff'
    s2.is_parallel = True

    seq = Container([s1, s2])

    r'''
    {
        \context Staff = "mystaff" <<
            \context Voice = "high" {
                c''8
                cs''8
                d''8
                ef''8
            }
            \context Voice = "low" {
                c'8
                cs'8
                d'8
                ef'8
            }
        >>
        \context Staff = "mystaff" <<
            \context Voice = "low" {
                e'8
                f'8
                fs'8
                g'8
            }
            \context Voice = "high" {
                e''8
                f''8
                fs''8
                g''8
            }
        >>
    }
    '''

    assert not vl1[3]._navigator._next_bead is vl2[0]
    assert not vh1[3]._navigator._next_bead is vh2[0]

    assert not vl2[0]._navigator._prev_bead is vl1[3]
    assert not vh2[0]._navigator._prev_bead is vh1[3]


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_12():
    '''Does connect through symmetrical nested containers in a voice.
    '''

    s1 = Container([Note(i, (1,8)) for i in range(4)])
    s1 = Container([s1])
    s2 = Container([Note(i, (1,8)) for i in range(4,8)])
    s2 = Container([s2])
    t = Voice([s1, s2])

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

    assert s1[0][0]._navigator._next_bead is s1[0][1]
    assert s1[0][1]._navigator._next_bead is s1[0][2]
    assert s1[0][2]._navigator._next_bead is s1[0][3]
    assert s1[0][3]._navigator._next_bead is s2[0][0]

    assert s2[0][1]._navigator._prev_bead is s2[0][0]
    assert s2[0][2]._navigator._prev_bead is s2[0][1]
    assert s2[0][3]._navigator._prev_bead is s2[0][2]
    assert s2[0][0]._navigator._prev_bead is s1[0][3]


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_13():
    '''Tautological parentage asymmetries result in symmetric (balanced) threaded parentage.
    '''

    s1 = Container([Note(i, (1,8)) for i in range(4)])
    s2 = Container([Note(i, (1,8)) for i in range(4,8)])
    s2 = Container([s2])
    s2 = Container([s2])
    t = Voice([s1, s2])

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

    assert s1[0]._navigator._next_bead is s1[1]
    assert s1[1]._navigator._next_bead is s1[2]
    assert s1[2]._navigator._next_bead is s1[3]
    assert s1[3]._navigator._next_bead is s2[0][0][0]

    assert s2[0][0][1]._navigator._prev_bead is s2[0][0][0]
    assert s2[0][0][2]._navigator._prev_bead is s2[0][0][1]
    assert s2[0][0][3]._navigator._prev_bead is s2[0][0][2]
    assert s2[0][0][0]._navigator._prev_bead is s1[3]


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_14():
    '''Tautological parentage asymmetries result in symmetric (balanced) threaded parentage.
    '''

    s1 = Container([Note(i, (1,8)) for i in range(4)])
    s1 = Container([s1])
    s1 = Container([s1])
    s2 = Container([Note(i, (1,8)) for i in range(4,8)])
    t = Voice([s1, s2])

    r'''
    \new Voice {
        {
            {
                {
                    c'8
                    cs'8
                    d'8
                    ef'8
                }
            }
        }
        {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''

    assert s1[0][0][0]._navigator._next_bead is s1[0][0][1]
    assert s1[0][0][1]._navigator._next_bead is s1[0][0][2]
    assert s1[0][0][2]._navigator._next_bead is s1[0][0][3]
    assert s1[0][0][3]._navigator._next_bead is s2[0]

    assert s2[0]._navigator._prev_bead is s1[0][0][3]
    assert s2[1]._navigator._prev_bead is s2[0]
    assert s2[2]._navigator._prev_bead is s2[1]
    assert s2[3]._navigator._prev_bead is s2[2]


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_15():
    '''Does connect in sequence of alternating containers and notes.
    '''

    s1 = Container([Note(i, (1,8)) for i in range(2)])
    s2 = Container([Note(i, (1,8)) for i in range(3,5)])
    v = Voice([s1, Note(2, (1,8)), s2])

    r'''
    \new Voice {
        {
            c'8
            cs'8
        }
        d'8
        {
            ef'8
            e'8
        }
    }
    '''

    assert s1[1]._navigator._next_bead is v[1]
    assert v[1]._navigator._next_bead is s2[0]

    assert v[1]._navigator._prev_bead is s1[1]
    assert s2[0]._navigator._prev_bead is v[1]


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_16():
    '''Does connect in sequence of alternating tuplets and notes.
    '''

    t1 = tuplettools.FixedDurationTuplet(Duration(1,4), [Note(i, (1,8)) for i in range(3)])
    t2 = tuplettools.FixedDurationTuplet(Duration(1,4), [Note(i, (1,8)) for i in range(4,7)])
    v = Voice([t1, Note(3, (1,8)), t2])

    r'''
    \new Voice {
        \times 2/3 {
            c'8
            cs'8
            d'8
        }
        ef'8
        \times 2/3 {
            e'8
            f'8
            fs'8
        }
    }
    '''

    assert t1[-1]._navigator._next_bead is v[1]
    assert v[1]._navigator._next_bead is t2[0]

    assert v[1]._navigator._prev_bead is t1[-1]
    assert t2[0]._navigator._prev_bead is v[1]


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_17():
    '''Does connect through asymmetrically nested tuplets.
    '''

    tinner = tuplettools.FixedDurationTuplet(Duration(1, 4), Note(0, (1, 8)) * 3)
    t = tuplettools.FixedDurationTuplet(Duration(2, 4), [Note("c'4"), tinner, Note("c'4")])

    r'''
    \times 2/3 {
        c'4
        \times 2/3 {
            c'8
            c'8
            c'8
        }
        c'4
    }
    '''

    assert t[0]._navigator._next_bead is tinner[0]
    assert tinner[-1]._navigator._next_bead is t[-1]
    assert t[-1]._navigator._prev_bead is tinner[-1]
    assert tinner[0]._navigator._prev_bead is t[0]


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_18():
    '''Return none in asymmetric thread parentage structures.
    '''

    v1 = Voice([Note(i , (1,8)) for i in range(3)])
    n = Note(3, (1,8))
    v2 = Voice([Note(i , (1,8)) for i in range(4,8)])
    t = Staff([v1, n, v2])

    r'''
    \new Staff {
        \new Voice {
            c'8
            cs'8
            d'8
        }
        ef'8
        \new Voice {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''

    assert v1[-1]._navigator._next_bead is None
    assert n._navigator._next_bead is None

    assert v2[0]._navigator._prev_bead is None
    assert n._navigator._prev_bead is None


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_19():
    '''Non-contiguous or broken threads do not connect.
    '''

    v1 = Voice([Note(i , (1,8)) for i in range(3)])
    v1.name = 'myvoice'
    v2 = Voice([Note(i , (1,8)) for i in range(4,8)])
    v2.name = 'yourvoice'
    v3 = Voice([Note(i , (1,8)) for i in range(4,8)])
    v3.name = 'myvoice'
    t = Staff([v1, v2, v3])

    r'''
    \new Staff {
        \context Voice = "myvoice" {
            c'8
            cs'8
            d'8
        }
        \context Voice = "yourvoice" {
            e'8
            f'8
            fs'8
            g'8
        }
        \context Voice = "myvoice" {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''

    assert v1[-1]._navigator._next_bead is None
    assert v2[-1]._navigator._next_bead is None
    v2.name = None
    assert v1[-1]._navigator._next_bead is None
    assert v2[-1]._navigator._next_bead is None

    assert v3[0]._navigator._prev_bead is None
    assert v2[0]._navigator._prev_bead is None


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_20():
    '''Does not connect through nested anonymous voices.
    '''

    vin = Voice([Note(i, (1,8)) for i in range(3)])
    vout = Voice([vin, Note(3, (1,8))])

    r'''
    \new Voice {
        \new Voice {
            c'8
            cs'8
            d'8
        }
        ef'8
    }
    '''

    assert vin[0]._navigator._next_bead is vin[1]
    assert vin[1]._navigator._next_bead is vin[2]
    assert vin[2]._navigator._next_bead is None

    assert vin[1]._navigator._prev_bead is vin[0]
    assert vin[2]._navigator._prev_bead is vin[1]
    assert vout[1]._navigator._prev_bead is None


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_21():
    '''Does not connec through nested anonymous voices.
    '''

    vin = Voice([Note(i, (1,8)) for i in range(1,4)])
    vout = Voice([Note(0, (1,8)), vin])

    r'''
    \new Voice {
        c'8
        \new Voice {
            cs'8
            d'8
            ef'8
        }
    }
    '''

    assert vin[0]._navigator._next_bead is vin[1]
    assert vin[1]._navigator._next_bead is vin[2]
    assert vout[0]._navigator._next_bead is None

    assert vin[1]._navigator._prev_bead is vin[0]
    assert vin[2]._navigator._prev_bead is vin[1]
    assert vin[0]._navigator._prev_bead is None



def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_22():
    '''Does connect through nested equally named voices.
    '''

    vin = Voice([Note(i, (1,8)) for i in range(3)])
    vin.name = 'myvoice'
    vout = Voice([vin, Note(3, (1,8))])
    vout.name = 'myvoice'

    r'''
    \context Voice = "myvoice" {
        \context Voice = "myvoice" {
            c'8
            cs'8
            d'8
        }
        ef'8
    }
    '''

    assert vin[0]._navigator._next_bead is vin[1]
    assert vin[1]._navigator._next_bead is vin[2]
    assert vin[2]._navigator._next_bead is vout[1]

    assert vin[1]._navigator._prev_bead is vin[0]
    assert vin[2]._navigator._prev_bead is vin[1]
    assert vout[1]._navigator._prev_bead is vin[-1]


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_23():
    '''Does connect through nested equally named voices.
    '''

    vin = Voice([Note(i, (1,8)) for i in range(1,4)])
    vin.name = 'myvoice'
    vout = Voice([Note(0, (1,8)), vin])
    vout.name = 'myvoice'

    r'''
    \context Voice = "myvoice" {
        c'8
        \context Voice = "myvoice" {
            cs'8
            d'8
            ef'8
        }
    }
    '''

    assert vin[0]._navigator._next_bead is vin[1]
    assert vin[1]._navigator._next_bead is vin[2]
    assert vout[0]._navigator._next_bead is vin[0]

    assert vin[1]._navigator._prev_bead is vin[0]
    assert vin[2]._navigator._prev_bead is vin[1]
    assert vin[0]._navigator._prev_bead is vout[0]


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_24():
    '''Return none on nested *differently* named voices.
    '''

    vin = Voice([Note(i, (1,8)) for i in range(3)])
    vin.name = 'yourvoice'
    vout = Voice([vin, Note(3, (1,8))])
    vout.name = 'myvoice'

    r'''
    \context Voice = "myvoice" {
        \context Voice = "yourvoice" {
            c'8
            cs'8
            d'8
        }
        ef'8
    }
    '''

    assert vin[0]._navigator._next_bead is vin[1]
    assert vin[1]._navigator._next_bead is vin[2]
    assert vin[2]._navigator._next_bead is None

    assert vin[1]._navigator._prev_bead is vin[0]
    assert vin[2]._navigator._prev_bead is vin[1]
    assert vout[1]._navigator._prev_bead is None


def test_leaftools_get_nth_leaf_in_thread_from_leaf_to_be_cleaned_up_25():
    '''Return none on nested *differently* named Voices.
    '''

    vin = Voice([Note(i, (1,8)) for i in range(1, 4)])
    vin.name = 'yourvoice'
    vout = Voice([Note(0, (1,8)), vin])
    vout.name = 'myvoice'

    r'''
    \context Voice = "myvoice" {
        c'8
        \context Voice = "yourvoice" {
            cs'8
            d'8
            ef'8
        }
    }
    '''

    assert vin[0]._navigator._next_bead is vin[1]
    assert vin[1]._navigator._next_bead is vin[2]
    assert vout[0]._navigator._next_bead is None

    assert vin[1]._navigator._prev_bead is vin[0]
    assert vin[2]._navigator._prev_bead is vin[1]
    assert vout[1]._navigator._prev_bead is None
