from abjad import *


# SIMPLE BEAD #

def test__NavigationInterface_bead_navigation_01( ):
    '''next_bead and prev_bead work on simple Voice.'''
    t = Voice([Note(i, (1,8)) for i in range(4)])
    assert t[0]._navigator._next_bead is t[1]
    assert t[1]._navigator._next_bead is t[2]
    assert t[2]._navigator._next_bead is t[3]
    assert t[3]._navigator._next_bead is None

    assert t[0]._navigator._prev_bead is None
    assert t[1]._navigator._prev_bead is t[0]
    assert t[2]._navigator._prev_bead is t[1]
    assert t[3]._navigator._prev_bead is t[2]

    r'''
    \new Voice {
        c'8
        cs'8
        d'8
        ef'8
    }
    '''


def test__NavigationInterface_bead_navigation_02( ):
    '''NextBead and prev_bead work on simple Staff.'''
    t = Staff([Note(i, (1,8)) for i in range(4)])
    assert t[0]._navigator._next_bead is t[1]
    assert t[1]._navigator._next_bead is t[2]
    assert t[2]._navigator._next_bead is t[3]
    assert t[3]._navigator._next_bead is None

    assert t[0]._navigator._prev_bead is None
    assert t[1]._navigator._prev_bead is t[0]
    assert t[2]._navigator._prev_bead is t[1]
    assert t[3]._navigator._prev_bead is t[2]

    r'''
    \new Staff {
        c'8
        cs'8
        d'8
        ef'8
    }
    '''


def test__NavigationInterface_bead_navigation_03( ):
    '''NextBead and prev_bead work on simple Container.'''
    t = Container([Note(i, (1,8)) for i in range(4)])
    assert t[0]._navigator._next_bead is t[1]
    assert t[1]._navigator._next_bead is t[2]
    assert t[2]._navigator._next_bead is t[3]
    assert t[3]._navigator._next_bead is None

    assert t[0]._navigator._prev_bead is None
    assert t[1]._navigator._prev_bead is t[0]
    assert t[2]._navigator._prev_bead is t[1]
    assert t[3]._navigator._prev_bead is t[2]

    r'''
    {
        c'8
        cs'8
        d'8
        ef'8
    }
    '''


# NONSTRUCTURAL in new parallel --> context model.
#def test__NavigationInterface_bead_navigation_04( ):
#   '''NextBead and prev_bead work on simple Parallel.'''
#   t = Container([Note(i, (1,8)) for i in range(4)])
#   t.is_parallel = True
#   assert t[0]._navigator._next_bead is None
#   assert t[1]._navigator._next_bead is None
#   assert t[2]._navigator._next_bead is None
#   assert t[3]._navigator._next_bead is None
#
#   assert t[0]._navigator._prev_bead is None
#   assert t[1]._navigator._prev_bead is None
#   assert t[2]._navigator._prev_bead is None
#   assert t[3]._navigator._prev_bead is None
#
#   r'''
#   <<
#      c'8
#      cs'8
#      d'8
#      ef'8
#   >>
#   '''


def test__NavigationInterface_bead_navigation_05( ):
    '''NextBead and prev_bead work on FixedDurationTuplet.'''
    t = tuplettools.FixedDurationTuplet(Duration(2,8), [Note(i, (1,8)) for i in range(3)])
    assert t[0]._navigator._next_bead is t[1]
    assert t[1]._navigator._next_bead is t[2]
    assert t[2]._navigator._next_bead is None

    assert t[0]._navigator._prev_bead is None
    assert t[1]._navigator._prev_bead is t[0]
    assert t[2]._navigator._prev_bead is t[1]

    r'''
    \times 2/3 {
        c'8
        cs'8
        d'8
    }
    '''


# LEVEL 1 NESTING #

def test__NavigationInterface_bead_navigation_06( ):
    '''NextBead and prev_bead work on contiguous Containers inside a Voice.'''
    s1 = Container([Note(i, (1,8)) for i in range(4)])
    s2 = Container([Note(i, (1,8)) for i in range(4,8)])
    t = Voice([s1, s2])
    assert s1[0]._navigator._next_bead is s1[1]
    assert s1[1]._navigator._next_bead is s1[2]
    assert s1[2]._navigator._next_bead is s1[3]
    assert s1[3]._navigator._next_bead is s2[0]

    assert s1[1]._navigator._prev_bead is s1[0]
    assert s1[2]._navigator._prev_bead is s1[1]
    assert s1[3]._navigator._prev_bead is s1[2]
    assert s2[0]._navigator._prev_bead is s1[3]

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


def test__NavigationInterface_bead_navigation_07( ):
    '''NextBead and prev_bead work on contiguous Tuplets inside a Voice.'''
    t1 = tuplettools.FixedDurationTuplet(Duration(2,8), [Note(i, (1,8)) for i in range(3)])
    t2 = tuplettools.FixedDurationTuplet(Duration(2,8), [Note(i, (1,8)) for i in range(3,6)])
    t = Voice([t1, t2])
    assert t1[0]._navigator._next_bead is t1[1]
    assert t1[1]._navigator._next_bead is t1[2]
    assert t1[2]._navigator._next_bead is t2[0]

    assert t1[1]._navigator._prev_bead is t1[0]
    assert t1[2]._navigator._prev_bead is t1[1]
    assert t2[0]._navigator._prev_bead is t1[2]

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


def test__NavigationInterface_bead_navigation_08( ):
    '''
    NextBead and prev_bead do not go across contiguous anonymous Voices
    inside a Staff.
    '''
    v1 = Voice([Note(i, (1,8)) for i in range(4)])
    v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
    t = Staff([v1, v2])
    assert v1[3]._navigator._next_bead is None
    assert v2[0]._navigator._prev_bead is None

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


def test__NavigationInterface_bead_navigation_09( ):
    '''NextBead and prev_bead work on contiguous equally named Voices
    inside a Staff.'''
    v1 = Voice([Note(i, (1,8)) for i in range(4)])
    v1.name = 'myvoice'
    v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
    v2.name = 'myvoice'
    t = Staff([v1, v2])
    assert v1[0]._navigator._next_bead is v1[1]
    assert v1[1]._navigator._next_bead is v1[2]
    assert v1[2]._navigator._next_bead is v1[3]
    assert v1[3]._navigator._next_bead is v2[0]

    assert v1[1]._navigator._prev_bead is v1[0]
    assert v1[2]._navigator._prev_bead is v1[1]
    assert v1[3]._navigator._prev_bead is v1[2]
    assert v2[0]._navigator._prev_bead is v1[3]

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


def test__NavigationInterface_bead_navigation_10( ):
    '''Beads do not connect through contiguous unequally named Voices;
    these are, by definition, two different "threads".'''
    v1 = Voice([Note(i, (1,8)) for i in range(4)])
    v1.name = 'yourvoice'
    v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
    v2.name = 'myvoice'
    t = Staff([v1, v2])
    assert v1[0]._navigator._next_bead is v1[1]
    assert v1[1]._navigator._next_bead is v1[2]
    assert v1[2]._navigator._next_bead is v1[3]
    assert v1[3]._navigator._next_bead is None
    v2.name = None
    assert v1[3]._navigator._next_bead is None

    assert v2[1]._navigator._prev_bead is v2[0]
    assert v2[2]._navigator._prev_bead is v2[1]
    assert v2[3]._navigator._prev_bead is v2[2]
    assert v2[0]._navigator._prev_bead is None

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


# LEVEL 2 NESTING #

def test__NavigationInterface_bead_navigation_11( ):
    '''Beads do NOT connect through equally named staves. '''

    v1 = Voice([Note(i, (1,8)) for i in range(4)])
    v1.name = 'low'
    v2 = Voice([Note(i, (1,8)) for i in range(4,8)])
    v2.name = 'low'

    s1 = Staff([v1])
    s1.name = 'mystaff'
    s2 = Staff([v2])
    s2.name = 'mystaff'

    seq = Container([s1, s2])

    assert not v1[3]._navigator._next_bead is v2[0]
    assert not v2[0]._navigator._prev_bead is v1[3]

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


def test__NavigationInterface_bead_navigation_12( ):
    '''Beads do NOT connect through equally named Staves.'''

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

    assert not vl1[3]._navigator._next_bead is vl2[0]
    assert not vh1[3]._navigator._next_bead is vh2[0]

    assert not vl2[0]._navigator._prev_bead is vl1[3]
    assert not vh2[0]._navigator._prev_bead is vh1[3]

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



# DEPTH ASYMMETRICAL STRUCTURES #
# Parentage asymmetrical structures work IF tautological #

def test__NavigationInterface_bead_navigation_13( ):
    '''next_bead and prev_bead work on symmetrical
        nested Containers in a Voice.'''
    s1 = Container([Note(i, (1,8)) for i in range(4)])
    s1 = Container([s1])
    s2 = Container([Note(i, (1,8)) for i in range(4,8)])
    s2 = Container([s2])
    t = Voice([s1, s2])
    assert s1[0][0]._navigator._next_bead is s1[0][1]
    assert s1[0][1]._navigator._next_bead is s1[0][2]
    assert s1[0][2]._navigator._next_bead is s1[0][3]
    assert s1[0][3]._navigator._next_bead is s2[0][0]

    assert s2[0][1]._navigator._prev_bead is s2[0][0]
    assert s2[0][2]._navigator._prev_bead is s2[0][1]
    assert s2[0][3]._navigator._prev_bead is s2[0][2]
    assert s2[0][0]._navigator._prev_bead is s1[0][3]

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


def test__NavigationInterface_bead_navigation_14( ):
    '''Tautological parentage asymmetries result in symmetric (balanced)
        threaded parentage.  These work well.'''
    s1 = Container([Note(i, (1,8)) for i in range(4)])
    s2 = Container([Note(i, (1,8)) for i in range(4,8)])
    s2 = Container([s2])
    s2 = Container([s2])
    t = Voice([s1, s2])
    assert s1[0]._navigator._next_bead is s1[1]
    assert s1[1]._navigator._next_bead is s1[2]
    assert s1[2]._navigator._next_bead is s1[3]
    assert s1[3]._navigator._next_bead is s2[0][0][0]

    assert s2[0][0][1]._navigator._prev_bead is s2[0][0][0]
    assert s2[0][0][2]._navigator._prev_bead is s2[0][0][1]
    assert s2[0][0][3]._navigator._prev_bead is s2[0][0][2]
    assert s2[0][0][0]._navigator._prev_bead is s1[3]

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


def test__NavigationInterface_bead_navigation_15( ):
    '''Tautological parentage asymmetries result in symmetric (balanced)
        threaded parentage.  These work well.'''
    s1 = Container([Note(i, (1,8)) for i in range(4)])
    s1 = Container([s1])
    s1 = Container([s1])
    s2 = Container([Note(i, (1,8)) for i in range(4,8)])
    t = Voice([s1, s2])
    assert s1[0][0][0]._navigator._next_bead is s1[0][0][1]
    assert s1[0][0][1]._navigator._next_bead is s1[0][0][2]
    assert s1[0][0][2]._navigator._next_bead is s1[0][0][3]
    assert s1[0][0][3]._navigator._next_bead is s2[0]

    assert s2[0]._navigator._prev_bead is s1[0][0][3]
    assert s2[1]._navigator._prev_bead is s2[0]
    assert s2[2]._navigator._prev_bead is s2[1]
    assert s2[3]._navigator._prev_bead is s2[2]

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


def test__NavigationInterface_bead_navigation_16( ):
    '''next_bead and prev_bead DO work in sequence of alternating
    Containers and Note.'''
    s1 = Container([Note(i, (1,8)) for i in range(2)])
    s2 = Container([Note(i, (1,8)) for i in range(3,5)])
    v = Voice([s1, Note(2, (1,8)), s2])
    assert s1[1]._navigator._next_bead is v[1]
    assert v[1]._navigator._next_bead is s2[0]

    assert v[1]._navigator._prev_bead is s1[1]
    assert s2[0]._navigator._prev_bead is v[1]

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


def test__NavigationInterface_bead_navigation_17( ):
    '''next_bead and prev_bead DO work in sequence of alternating
    tuplets and Notes.'''
    t1 = tuplettools.FixedDurationTuplet(Duration(1,4), [Note(i, (1,8)) for i in range(3)])
    t2 = tuplettools.FixedDurationTuplet(Duration(1,4), [Note(i, (1,8)) for i in range(4,7)])
    v = Voice([t1, Note(3, (1,8)), t2])
    assert t1[-1]._navigator._next_bead is v[1]
    assert v[1]._navigator._next_bead is t2[0]

    assert v[1]._navigator._prev_bead is t1[-1]
    assert t2[0]._navigator._prev_bead is v[1]

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


def test__NavigationInterface_bead_navigation_18( ):
    '''next_bead and prev_bead  work on asymmetrically nested tuplets.'''
    tinner = tuplettools.FixedDurationTuplet(Duration(1, 4), Note(0, (1, 8)) * 3)
    t = tuplettools.FixedDurationTuplet(Duration(2, 4), [Note("c'4"), tinner, Note("c'4")])
    assert t[0]._navigator._next_bead is tinner[0]
    assert tinner[-1]._navigator._next_bead is t[-1]
    assert t[-1]._navigator._prev_bead is tinner[-1]
    assert tinner[0]._navigator._prev_bead is t[0]
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


# Parentage asymmetrical structures DON'T work if NOT tautological #

def test__NavigationInterface_bead_navigation_19( ):
    '''NextBead returns None in asymmetric thread parentage structures.'''
    v1 = Voice([Note(i , (1,8)) for i in range(3)])
    n = Note(3, (1,8))
    v2 = Voice([Note(i , (1,8)) for i in range(4,8)])
    t = Staff([v1, n, v2])
    assert v1[-1]._navigator._next_bead is None
    assert n._navigator._next_bead is None

    assert v2[0]._navigator._prev_bead is None
    assert n._navigator._prev_bead is None

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


# NON-CONTIGUOUS / BROKEN THREADS #

def test__NavigationInterface_bead_navigation_20( ):
    '''Non-contiguous / broken threads do not connect.'''
    #
    # do we want them to connect? probably not...
    #
    v1 = Voice([Note(i , (1,8)) for i in range(3)])
    v1.name = 'myvoice'
    v2 = Voice([Note(i , (1,8)) for i in range(4,8)])
    v2.name = 'yourvoice'
    v3 = Voice([Note(i , (1,8)) for i in range(4,8)])
    v3.name = 'myvoice'
    t = Staff([v1, v2, v3])

    assert v1[-1]._navigator._next_bead is None
    assert v2[-1]._navigator._next_bead is None
    v2.name = None
    assert v1[-1]._navigator._next_bead is None
    assert v2[-1]._navigator._next_bead is None

    assert v3[0]._navigator._prev_bead is None
    assert v2[0]._navigator._prev_bead is None

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


# TAUTOLOGICAL NESTING #

def test__NavigationInterface_bead_navigation_21( ):
    '''
    next_bead and prev_bead do not work on nested anonymous Voices.
    '''
    vin = Voice([Note(i, (1,8)) for i in range(3)])
    vout = Voice([vin, Note(3, (1,8))])
    assert vin[0]._navigator._next_bead is vin[1]
    assert vin[1]._navigator._next_bead is vin[2]
    assert vin[2]._navigator._next_bead is None

    assert vin[1]._navigator._prev_bead is vin[0]
    assert vin[2]._navigator._prev_bead is vin[1]
    assert vout[1]._navigator._prev_bead is None

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


def test__NavigationInterface_bead_navigation_22( ):
    '''next_bead and prev_bead do not work on nested anonymous Voices.'''
    vin = Voice([Note(i, (1,8)) for i in range(1,4)])
    vout = Voice([Note(0, (1,8)), vin])
    assert vin[0]._navigator._next_bead is vin[1]
    assert vin[1]._navigator._next_bead is vin[2]
    assert vout[0]._navigator._next_bead is None

    assert vin[1]._navigator._prev_bead is vin[0]
    assert vin[2]._navigator._prev_bead is vin[1]
    assert vin[0]._navigator._prev_bead is None

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



def test__NavigationInterface_bead_navigation_23( ):
    '''next_bead and prev_bead work on nested equally named Voices.'''
    vin = Voice([Note(i, (1,8)) for i in range(3)])
    vin.name = 'myvoice'
    vout = Voice([vin, Note(3, (1,8))])
    vout.name = 'myvoice'
    assert vin[0]._navigator._next_bead is vin[1]
    assert vin[1]._navigator._next_bead is vin[2]
    assert vin[2]._navigator._next_bead is vout[1]

    assert vin[1]._navigator._prev_bead is vin[0]
    assert vin[2]._navigator._prev_bead is vin[1]
    assert vout[1]._navigator._prev_bead is vin[-1]

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


def test__NavigationInterface_bead_navigation_24( ):
    '''next_bead and prev_bead work on nested equally named Voices.'''
    vin = Voice([Note(i, (1,8)) for i in range(1,4)])
    vin.name = 'myvoice'
    vout = Voice([Note(0, (1,8)), vin])
    vout.name = 'myvoice'
    assert vin[0]._navigator._next_bead is vin[1]
    assert vin[1]._navigator._next_bead is vin[2]
    assert vout[0]._navigator._next_bead is vin[0]

    assert vin[1]._navigator._prev_bead is vin[0]
    assert vin[2]._navigator._prev_bead is vin[1]
    assert vin[0]._navigator._prev_bead is vout[0]

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


def test__NavigationInterface_bead_navigation_25( ):
    '''NextBead return None on nested *differently* named Voices.
        This is what we want because these are NOT tautologies.'''
    vin = Voice([Note(i, (1,8)) for i in range(3)])
    vin.name = 'yourvoice'
    vout = Voice([vin, Note(3, (1,8))])
    vout.name = 'myvoice'
    assert vin[0]._navigator._next_bead is vin[1]
    assert vin[1]._navigator._next_bead is vin[2]
    assert vin[2]._navigator._next_bead is None

    assert vin[1]._navigator._prev_bead is vin[0]
    assert vin[2]._navigator._prev_bead is vin[1]
    assert vout[1]._navigator._prev_bead is None

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


def test__NavigationInterface_bead_navigation_26( ):
    '''NextBead return None on nested *differently* named Voices.
        This is what we want because these are NOT tautologies.'''
    vin = Voice([Note(i, (1,8)) for i in range(1, 4)])
    vin.name = 'yourvoice'
    vout = Voice([Note(0, (1,8)), vin])
    vout.name = 'myvoice'
    assert vin[0]._navigator._next_bead is vin[1]
    assert vin[1]._navigator._next_bead is vin[2]
    assert vout[0]._navigator._next_bead is None

    assert vin[1]._navigator._prev_bead is vin[0]
    assert vin[2]._navigator._prev_bead is vin[1]
    assert vout[1]._navigator._prev_bead is None

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
