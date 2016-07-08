# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_InspectionAgent_get_leaf_01():

    staff = Staff([Voice("c'8 d'8 e'8 f'8"), Voice("g'8 a'8 b'8 c''8")])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \new Voice {
                c'8
                d'8
                e'8
                f'8
            }
            \new Voice {
                g'8
                a'8
                b'8
                c''8
            }
        }
        '''
        )

    leaves = select(staff).by_leaf()
    assert inspect_(leaves[0]).get_leaf(0) is leaves[0]
    assert inspect_(leaves[0]).get_leaf(1) is leaves[1]
    assert inspect_(leaves[0]).get_leaf(2) is leaves[2]
    assert inspect_(leaves[0]).get_leaf(3) is leaves[3]
    assert inspect_(leaves[0]).get_leaf(4) is None
    assert inspect_(leaves[0]).get_leaf(5) is None
    assert inspect_(leaves[0]).get_leaf(6) is None
    assert inspect_(leaves[0]).get_leaf(7) is None

    assert inspect_(leaves[0]).get_leaf(-1) is None


def test_agenttools_InspectionAgent_get_leaf_02():
    r'''Voice.
    '''

    voice = Voice([Note(i, (1, 8)) for i in range(4)])

    assert inspect_(voice[0]).get_leaf(1) is voice[1]
    assert inspect_(voice[1]).get_leaf(1) is voice[2]
    assert inspect_(voice[2]).get_leaf(1) is voice[3]
    assert inspect_(voice[3]).get_leaf(1) is None

    assert inspect_(voice[0]).get_leaf(-1) is None
    assert inspect_(voice[1]).get_leaf(-1) is voice[0]
    assert inspect_(voice[2]).get_leaf(-1) is voice[1]
    assert inspect_(voice[3]).get_leaf(-1) is voice[2]

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8
            cs'8
            d'8
            ef'8
        }
        '''
        )


def test_agenttools_InspectionAgent_get_leaf_03():
    r'''Staff.
    '''

    staff = Staff([Note(i, (1, 8)) for i in range(4)])

    assert inspect_(staff[0]).get_leaf(1) is staff[1]
    assert inspect_(staff[1]).get_leaf(1) is staff[2]
    assert inspect_(staff[2]).get_leaf(1) is staff[3]
    assert inspect_(staff[3]).get_leaf(1) is None

    assert inspect_(staff[0]).get_leaf(-1) is None
    assert inspect_(staff[1]).get_leaf(-1) is staff[0]
    assert inspect_(staff[2]).get_leaf(-1) is staff[1]
    assert inspect_(staff[3]).get_leaf(-1) is staff[2]

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8
            cs'8
            d'8
            ef'8
        }
        '''
        )


def test_agenttools_InspectionAgent_get_leaf_04():
    r'''Container.
    '''

    container = Container([Note(i, (1, 8)) for i in range(4)])

    assert format(container) == stringtools.normalize(
        r'''
        {
            c'8
            cs'8
            d'8
            ef'8
        }
        '''
        )

    assert inspect_(container[0]).get_leaf(1) is container[1]
    assert inspect_(container[1]).get_leaf(1) is container[2]
    assert inspect_(container[2]).get_leaf(1) is container[3]
    assert inspect_(container[3]).get_leaf(1) is None

    assert inspect_(container[0]).get_leaf(-1) is None
    assert inspect_(container[1]).get_leaf(-1) is container[0]
    assert inspect_(container[2]).get_leaf(-1) is container[1]
    assert inspect_(container[3]).get_leaf(-1) is container[2]


def test_agenttools_InspectionAgent_get_leaf_05():
    r'''Fixed-duration tuplet.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 cs'8 d'8")

    assert format(tuplet) == stringtools.normalize(
        r'''
        \times 2/3 {
            c'8
            cs'8
            d'8
        }
        '''
        )

    assert inspect_(tuplet[0]).get_leaf(1) is tuplet[1]
    assert inspect_(tuplet[1]).get_leaf(1) is tuplet[2]
    assert inspect_(tuplet[2]).get_leaf(1) is None

    assert inspect_(tuplet[0]).get_leaf(-1) is None
    assert inspect_(tuplet[1]).get_leaf(-1) is tuplet[0]
    assert inspect_(tuplet[2]).get_leaf(-1) is tuplet[1]


def test_agenttools_InspectionAgent_get_leaf_06():
    r'''Contiguous containers inside a voice.
    '''

    container_1 = Container([Note(i, (1, 8)) for i in range(4)])
    container_2 = Container([Note(i, (1, 8)) for i in range(4, 8)])
    voice = Voice([container_1, container_2])

    assert format(voice) == stringtools.normalize(
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
        )

    assert inspect_(container_1[0]).get_leaf(1) is container_1[1]
    assert inspect_(container_1[1]).get_leaf(1) is container_1[2]
    assert inspect_(container_1[2]).get_leaf(1) is container_1[3]
    assert inspect_(container_1[3]).get_leaf(1) is container_2[0]

    assert inspect_(container_1[1]).get_leaf(-1) is container_1[0]
    assert inspect_(container_1[2]).get_leaf(-1) is container_1[1]
    assert inspect_(container_1[3]).get_leaf(-1) is container_1[2]
    assert inspect_(container_2[0]).get_leaf(-1) is container_1[3]


def test_agenttools_InspectionAgent_get_leaf_07():
    r'''Tuplets inside a voice.
    '''

    tuplet_1 = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 cs'8 d'8")
    tuplet_2 = scoretools.FixedDurationTuplet(Duration(2, 8), "ef'8 e'8 f'8")
    voice = Voice([tuplet_1, tuplet_2])

    assert format(voice) == stringtools.normalize(
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
        )

    assert inspect_(tuplet_1[0]).get_leaf(1) is tuplet_1[1]
    assert inspect_(tuplet_1[1]).get_leaf(1) is tuplet_1[2]
    assert inspect_(tuplet_1[2]).get_leaf(1) is tuplet_2[0]

    assert inspect_(tuplet_1[1]).get_leaf(-1) is tuplet_1[0]
    assert inspect_(tuplet_1[2]).get_leaf(-1) is tuplet_1[1]
    assert inspect_(tuplet_2[0]).get_leaf(-1) is tuplet_1[2]


def test_agenttools_InspectionAgent_get_leaf_08():
    r'''Does not continue across contiguous anonymous voices inside a staff.
    '''

    voice_1 = Voice([Note(i, (1, 8)) for i in range(4)])
    voice_2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
    staff = Staff([voice_1, voice_2])

    assert format(staff) == stringtools.normalize(
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
        )

    assert inspect_(voice_1[3]).get_leaf(1) is None
    assert inspect_(voice_2[0]).get_leaf(-1) is None


def test_agenttools_InspectionAgent_get_leaf_09():
    r'''Does cross contiguous equally named voices inside a staff.
    '''

    voice_1 = Voice([Note(i, (1, 8)) for i in range(4)])
    voice_1.name = 'My Voice'
    voice_2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
    voice_2.name = 'My Voice'
    staff = Staff([voice_1, voice_2])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \context Voice = "My Voice" {
                c'8
                cs'8
                d'8
                ef'8
            }
            \context Voice = "My Voice" {
                e'8
                f'8
                fs'8
                g'8
            }
        }
        '''
        )

    assert inspect_(voice_1[0]).get_leaf(1) is voice_1[1]
    assert inspect_(voice_1[1]).get_leaf(1) is voice_1[2]
    assert inspect_(voice_1[2]).get_leaf(1) is voice_1[3]
    assert inspect_(voice_1[3]).get_leaf(1) is voice_2[0]

    assert inspect_(voice_1[1]).get_leaf(-1) is voice_1[0]
    assert inspect_(voice_1[2]).get_leaf(-1) is voice_1[1]
    assert inspect_(voice_1[3]).get_leaf(-1) is voice_1[2]
    assert inspect_(voice_2[0]).get_leaf(-1) is voice_1[3]


def test_agenttools_InspectionAgent_get_leaf_10():
    r'''Does not connect through contiguous unequally named voices.
    '''

    voice_1 = Voice([Note(i, (1, 8)) for i in range(4)])
    voice_1.name = 'Your Voice'
    voice_2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
    voice_2.name = 'My Voice'
    staff = Staff([voice_1, voice_2])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \context Voice = "Your Voice" {
                c'8
                cs'8
                d'8
                ef'8
            }
            \context Voice = "My Voice" {
                e'8
                f'8
                fs'8
                g'8
            }
        }
        '''
        )

    assert inspect_(voice_1[0]).get_leaf(1) is voice_1[1]
    assert inspect_(voice_1[1]).get_leaf(1) is voice_1[2]
    assert inspect_(voice_1[2]).get_leaf(1) is voice_1[3]
    assert inspect_(voice_1[3]).get_leaf(1) is None

    voice_2.name = None
    assert inspect_(voice_1[3]).get_leaf(1) is None

    assert inspect_(voice_2[1]).get_leaf(-1) is voice_2[0]
    assert inspect_(voice_2[2]).get_leaf(-1) is voice_2[1]
    assert inspect_(voice_2[3]).get_leaf(-1) is voice_2[2]
    assert inspect_(voice_2[0]).get_leaf(-1) is None


def test_agenttools_InspectionAgent_get_leaf_11():
    r'''Does connect through like-named staves
    containing like-named voices.
    '''

    voice_1 = Voice([Note(i, (1, 8)) for i in range(4)])
    voice_1.name = 'low'
    voice_2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
    voice_2.name = 'low'

    staff_1 = Staff([voice_1])
    staff_1.name = 'mystaff'
    staff_2 = Staff([voice_2])
    staff_2.name = 'mystaff'

    container = Container([staff_1, staff_2])

    assert format(container) == stringtools.normalize(
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
        )

    assert inspect_(voice_1[3]).get_leaf(1) is voice_2[0]
    assert inspect_(voice_2[0]).get_leaf(-1) is voice_1[3]


def test_agenttools_InspectionAgent_get_leaf_12():
    r'''Does connect through like-named staves containing
    like-named voices.
    '''

    lower_voice_1 = Voice([Note(i, (1, 8)) for i in range(4)])
    lower_voice_1.name = 'low'
    lower_voice_2 = Voice([Note(i, (1, 8)) for i in range(4 ,8)])
    lower_voice_2.name = 'low'
    higher_voice_1 = Voice([Note(i, (1 ,8)) for i in range(12,16)])
    higher_voice_1.name = 'high'
    higher_voice_2 = Voice([Note(i, (1 ,8)) for i in range(16,20)])
    higher_voice_2.name = 'high'

    staff_1 = Staff([higher_voice_1, lower_voice_1])
    staff_1.name = 'mystaff'
    staff_1.is_simultaneous = True
    staff_2 = Staff([lower_voice_2, higher_voice_2])
    staff_2.name = 'mystaff'
    staff_2.is_simultaneous = True

    container = Container([staff_1, staff_2])

    assert format(container) == stringtools.normalize(
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
        )

    assert inspect_(lower_voice_1[3]).get_leaf(1) is lower_voice_2[0]
    assert inspect_(higher_voice_1[3]).get_leaf(1) is higher_voice_2[0]

    assert inspect_(lower_voice_2[0]).get_leaf(-1) is lower_voice_1[3]
    assert inspect_(higher_voice_2[0]).get_leaf(-1) is higher_voice_1[3]


def test_agenttools_InspectionAgent_get_leaf_13():
    r'''Does connect through symmetrical nested containers in a voice.
    '''

    container_1 = Container([Note(i, (1 ,8)) for i in range(4)])
    container_1 = Container([container_1])
    container_2 = Container([Note(i, (1 ,8)) for i in range(4 ,8)])
    container_2 = Container([container_2])
    voice = Voice([container_1, container_2])

    assert format(voice) == stringtools.normalize(
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
        )

    assert inspect_(container_1[0][0]).get_leaf(1) is container_1[0][1]
    assert inspect_(container_1[0][1]).get_leaf(1) is container_1[0][2]
    assert inspect_(container_1[0][2]).get_leaf(1) is container_1[0][3]
    assert inspect_(container_1[0][3]).get_leaf(1) is container_2[0][0]

    assert inspect_(container_2[0][1]).get_leaf(-1) is container_2[0][0]
    assert inspect_(container_2[0][2]).get_leaf(-1) is container_2[0][1]
    assert inspect_(container_2[0][3]).get_leaf(-1) is container_2[0][2]
    assert inspect_(container_2[0][0]).get_leaf(-1) is container_1[0][3]


def test_agenttools_InspectionAgent_get_leaf_14():
    r'''Tautological parentage asymmetries result in symmetric (balanced)
    logical voice parentage.
    '''

    container_1 = Container([Note(i, (1 ,8)) for i in range(4)])
    container_2 = Container([Note(i, (1 ,8)) for i in range(4 ,8)])
    container_2 = Container([container_2])
    container_2 = Container([container_2])
    voice = Voice([container_1, container_2])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8
                cs'8
                d'8
                ef'8
            }
            {
                {
                    {
                        e'8
                        f'8
                        fs'8
                        g'8
                    }
                }
            }
        }
        '''
        )

    assert inspect_(container_1[0]).get_leaf(1) is container_1[1]
    assert inspect_(container_1[1]).get_leaf(1) is container_1[2]
    assert inspect_(container_1[2]).get_leaf(1) is container_1[3]
    assert inspect_(container_1[3]).get_leaf(1) is container_2[0][0][0]

    assert inspect_(container_2[0][0][1]).get_leaf(-1) is container_2[0][0][0]
    assert inspect_(container_2[0][0][2]).get_leaf(-1) is container_2[0][0][1]
    assert inspect_(container_2[0][0][3]).get_leaf(-1) is container_2[0][0][2]
    assert inspect_(container_2[0][0][0]).get_leaf(-1) is container_1[3]


def test_agenttools_InspectionAgent_get_leaf_15():
    r'''Tautological parentage asymmetries result in symmetric (balanced)
    lgoical voice parentage.
    '''

    container_1 = Container([Note(i, (1 ,8)) for i in range(4)])
    container_1 = Container([container_1])
    container_1 = Container([container_1])
    container_2 = Container([Note(i, (1 ,8)) for i in range(4 ,8)])
    voice = Voice([container_1, container_2])

    assert format(voice) == stringtools.normalize(
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
        )

    assert inspect_(container_1[0][0][0]).get_leaf(1) is container_1[0][0][1]
    assert inspect_(container_1[0][0][1]).get_leaf(1) is container_1[0][0][2]
    assert inspect_(container_1[0][0][2]).get_leaf(1) is container_1[0][0][3]
    assert inspect_(container_1[0][0][3]).get_leaf(1) is container_2[0]

    assert inspect_(container_2[0]).get_leaf(-1) is container_1[0][0][3]
    assert inspect_(container_2[1]).get_leaf(-1) is container_2[0]
    assert inspect_(container_2[2]).get_leaf(-1) is container_2[1]
    assert inspect_(container_2[3]).get_leaf(-1) is container_2[2]


def test_agenttools_InspectionAgent_get_leaf_16():
    r'''Does connect in sequence of alternating containers and notes.
    '''

    container_1 = Container([Note(i, (1, 8)) for i in range(2)])
    container_2 = Container([Note(i, (1, 8)) for i in range(3, 5)])
    voice = Voice([container_1, Note(2, (1, 8)), container_2])

    assert format(voice) == stringtools.normalize(
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
        )

    assert inspect_(container_1[1]).get_leaf(1) is voice[1]
    assert inspect_(voice[1]).get_leaf(1) is container_2[0]

    assert inspect_(voice[1]).get_leaf(-1) is container_1[1]
    assert inspect_(container_2[0]).get_leaf(-1) is voice[1]


def test_agenttools_InspectionAgent_get_leaf_17():
    r'''Does connect in sequence of alternating tuplets and notes.
    '''

    notes = [Note(i, Duration(1, 8)) for i in range(3)]
    tuplet_1 = scoretools.FixedDurationTuplet(Duration(1, 4), notes)
    notes = [Note(i, Duration(1, 8)) for i in range(4, 7)]
    tuplet_2 = scoretools.FixedDurationTuplet(Duration(1, 4), notes)
    voice = Voice([tuplet_1, Note(3, (1, 8)), tuplet_2])

    assert format(voice) == stringtools.normalize(
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
        )

    assert inspect_(tuplet_1[-1]).get_leaf(1) is voice[1]
    assert inspect_(voice[1]).get_leaf(1) is tuplet_2[0]

    assert inspect_(voice[1]).get_leaf(-1) is tuplet_1[-1]
    assert inspect_(tuplet_2[0]).get_leaf(-1) is voice[1]


def test_agenttools_InspectionAgent_get_leaf_18():
    r'''Does connect through asymmetrically nested tuplets.
    '''

    inner_tuplet = scoretools.FixedDurationTuplet((1, 4), "c'8 c'8 c'8")
    contents = [Note("c'4"), inner_tuplet, Note("c'4")]
    tuplet = scoretools.FixedDurationTuplet(Duration(2, 4), contents)

    assert format(tuplet) == stringtools.normalize(
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
        )

    assert inspect_(tuplet[0]).get_leaf(1) is inner_tuplet[0]
    assert inspect_(inner_tuplet[-1]).get_leaf(1) is tuplet[-1]
    assert inspect_(tuplet[-1]).get_leaf(-1) is inner_tuplet[-1]
    assert inspect_(inner_tuplet[0]).get_leaf(-1) is tuplet[0]


def test_agenttools_InspectionAgent_get_leaf_19():
    r'''Returns none in asymmetric logical voice parentage structures.
    '''

    voice_1 = Voice([Note(i, (1, 8)) for i in range(3)])
    note = Note(3, (1, 8))
    voice_2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
    staff = Staff([voice_1, note, voice_2])

    assert format(staff) == stringtools.normalize(
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
        )

    assert inspect_(voice_1[-1]).get_leaf(1) is None
    assert inspect_(note).get_leaf(1) is None

    assert inspect_(voice_2[0]).get_leaf(-1) is None
    assert inspect_(note).get_leaf(-1) is None


def test_agenttools_InspectionAgent_get_leaf_20():
    r'''Noncontiguous or broken logical voices do not connect.
    '''

    voice_1 = Voice([Note(i, (1, 8)) for i in range(3)])
    voice_1.name = 'My Voice'
    voice_2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
    voice_2.name = 'Your Voice'
    voice_3 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
    voice_3.name = 'My Voice'
    staff = Staff([voice_1, voice_2, voice_3])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \context Voice = "My Voice" {
                c'8
                cs'8
                d'8
            }
            \context Voice = "Your Voice" {
                e'8
                f'8
                fs'8
                g'8
            }
            \context Voice = "My Voice" {
                e'8
                f'8
                fs'8
                g'8
            }
        }
        '''
        )

    assert inspect_(voice_1[-1]).get_leaf(1) is None
    assert inspect_(voice_2[-1]).get_leaf(1) is None

    voice_2.name = None

    assert inspect_(voice_1[-1]).get_leaf(1) is None
    assert inspect_(voice_2[-1]).get_leaf(1) is None

    assert inspect_(voice_3[0]).get_leaf(-1) is None
    assert inspect_(voice_2[0]).get_leaf(-1) is None


def test_agenttools_InspectionAgent_get_leaf_21():
    r'''Does not connect through nested anonymous voices.
    '''

    inner_voice = Voice([Note(i, (1, 8)) for i in range(3)])
    outer_voice = Voice([inner_voice, Note(3, (1, 8))])

    assert format(outer_voice) == stringtools.normalize(
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
        )

    assert inspect_(inner_voice[0]).get_leaf(1) is inner_voice[1]
    assert inspect_(inner_voice[1]).get_leaf(1) is inner_voice[2]
    assert inspect_(inner_voice[2]).get_leaf(1) is None

    assert inspect_(inner_voice[1]).get_leaf(-1) is inner_voice[0]
    assert inspect_(inner_voice[2]).get_leaf(-1) is inner_voice[1]
    assert inspect_(outer_voice[1]).get_leaf(-1) is None


def test_agenttools_InspectionAgent_get_leaf_22():
    r'''Does not connect through nested anonymous voices.
    '''

    inner_voice = Voice([Note(i, (1, 8)) for i in range(1, 4)])
    outer_voice = Voice([Note(0, (1, 8)), inner_voice])

    assert format(outer_voice) == stringtools.normalize(
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
        )

    assert inspect_(inner_voice[0]).get_leaf(1) is inner_voice[1]
    assert inspect_(inner_voice[1]).get_leaf(1) is inner_voice[2]
    assert inspect_(outer_voice[0]).get_leaf(1) is None

    assert inspect_(inner_voice[1]).get_leaf(-1) is inner_voice[0]
    assert inspect_(inner_voice[2]).get_leaf(-1) is inner_voice[1]
    assert inspect_(inner_voice[0]).get_leaf(-1) is None



def test_agenttools_InspectionAgent_get_leaf_23():
    r'''Does connect through nested equally named voices.
    '''

    inner_voice = Voice([Note(i, (1, 8)) for i in range(3)])
    inner_voice.name = 'My Voice'
    outer_voice = Voice([inner_voice, Note(3, (1, 8))])
    outer_voice.name = 'My Voice'

    assert format(outer_voice) == stringtools.normalize(
        r'''
        \context Voice = "My Voice" {
            \context Voice = "My Voice" {
                c'8
                cs'8
                d'8
            }
            ef'8
        }
        '''
        )

    assert inspect_(inner_voice[0]).get_leaf(1) is inner_voice[1]
    assert inspect_(inner_voice[1]).get_leaf(1) is inner_voice[2]
    assert inspect_(inner_voice[2]).get_leaf(1) is outer_voice[1]

    assert inspect_(inner_voice[1]).get_leaf(-1) is inner_voice[0]
    assert inspect_(inner_voice[2]).get_leaf(-1) is inner_voice[1]
    assert inspect_(outer_voice[1]).get_leaf(-1) is inner_voice[-1]


def test_agenttools_InspectionAgent_get_leaf_24():
    r'''Does connect through nested equally named voices.
    '''

    inner_voice = Voice([Note(i, (1, 8)) for i in range(1, 4)])
    inner_voice.name = 'My Voice'
    outer_voice = Voice([Note(0, (1, 8)), inner_voice])
    outer_voice.name = 'My Voice'

    assert format(outer_voice) == stringtools.normalize(
        r'''
        \context Voice = "My Voice" {
            c'8
            \context Voice = "My Voice" {
                cs'8
                d'8
                ef'8
            }
        }
        '''
        )

    assert inspect_(inner_voice[0]).get_leaf(1) is inner_voice[1]
    assert inspect_(inner_voice[1]).get_leaf(1) is inner_voice[2]
    assert inspect_(outer_voice[0]).get_leaf(1) is inner_voice[0]

    assert inspect_(inner_voice[1]).get_leaf(-1) is inner_voice[0]
    assert inspect_(inner_voice[2]).get_leaf(-1) is inner_voice[1]
    assert inspect_(inner_voice[0]).get_leaf(-1) is outer_voice[0]


def test_agenttools_InspectionAgent_get_leaf_25():
    r'''Returns none on nested differently named voices.
    '''

    inner_voice = Voice([Note(i, (1, 8)) for i in range(3)])
    inner_voice.name = 'Your Voice'
    outer_voice = Voice([inner_voice, Note(3, (1, 8))])
    outer_voice.name = 'My Voice'

    assert format(outer_voice) == stringtools.normalize(
        r'''
        \context Voice = "My Voice" {
            \context Voice = "Your Voice" {
                c'8
                cs'8
                d'8
            }
            ef'8
        }
        '''
        )

    assert inspect_(inner_voice[0]).get_leaf(1) is inner_voice[1]
    assert inspect_(inner_voice[1]).get_leaf(1) is inner_voice[2]
    assert inspect_(inner_voice[2]).get_leaf(1) is None

    assert inspect_(inner_voice[1]).get_leaf(-1) is inner_voice[0]
    assert inspect_(inner_voice[2]).get_leaf(-1) is inner_voice[1]
    assert inspect_(outer_voice[1]).get_leaf(-1) is None


def test_agenttools_InspectionAgent_get_leaf_26():
    r'''Returns none on nested differently named voices.
    '''

    voice_2 = Voice([Note(i, (1, 8)) for i in range(1, 4)])
    voice_2.name = 'Voice 2'
    voice_1 = Voice([Note(0, (1, 8)), voice_2])
    voice_1.name = 'Voice 1'

    assert format(voice_1) == stringtools.normalize(
        r'''
        \context Voice = "Voice 1" {
            c'8
            \context Voice = "Voice 2" {
                cs'8
                d'8
                ef'8
            }
        }
        '''
        )

    assert inspect_(voice_2[0]).get_leaf(1) is voice_2[1]
    assert inspect_(voice_2[1]).get_leaf(1) is voice_2[2]
    assert inspect_(voice_1[0]).get_leaf(1) is None

    assert inspect_(voice_2[1]).get_leaf(-1) is voice_2[0]
    assert inspect_(voice_2[2]).get_leaf(-1) is voice_2[1]
    assert inspect_(voice_1[1]).get_leaf(-1) is voice_2[-1]
