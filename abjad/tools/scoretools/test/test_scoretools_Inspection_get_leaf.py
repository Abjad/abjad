import abjad


def test_scoretools_Inspection_get_leaf_01():

    staff = abjad.Staff([abjad.Voice("c'8 d'8 e'8 f'8"), abjad.Voice("g'8 a'8 b'8 c''8")])

    assert format(staff) == abjad.String.normalize(
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

    leaves = abjad.select(staff).leaves()
    assert abjad.inspect(leaves[0]).get_leaf(0) is leaves[0]
    assert abjad.inspect(leaves[0]).get_leaf(1) is leaves[1]
    assert abjad.inspect(leaves[0]).get_leaf(2) is leaves[2]
    assert abjad.inspect(leaves[0]).get_leaf(3) is leaves[3]
    assert abjad.inspect(leaves[0]).get_leaf(4) is None
    assert abjad.inspect(leaves[0]).get_leaf(5) is None
    assert abjad.inspect(leaves[0]).get_leaf(6) is None
    assert abjad.inspect(leaves[0]).get_leaf(7) is None

    assert abjad.inspect(leaves[0]).get_leaf(-1) is None


def test_scoretools_Inspection_get_leaf_02():
    r'''Voice.
    '''

    voice = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4)])

    assert abjad.inspect(voice[0]).get_leaf(1) is voice[1]
    assert abjad.inspect(voice[1]).get_leaf(1) is voice[2]
    assert abjad.inspect(voice[2]).get_leaf(1) is voice[3]
    assert abjad.inspect(voice[3]).get_leaf(1) is None

    assert abjad.inspect(voice[0]).get_leaf(-1) is None
    assert abjad.inspect(voice[1]).get_leaf(-1) is voice[0]
    assert abjad.inspect(voice[2]).get_leaf(-1) is voice[1]
    assert abjad.inspect(voice[3]).get_leaf(-1) is voice[2]

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8
            cs'8
            d'8
            ef'8
        }
        '''
        )


def test_scoretools_Inspection_get_leaf_03():
    r'''Staff.
    '''

    staff = abjad.Staff([abjad.Note(i, (1, 8)) for i in range(4)])

    assert abjad.inspect(staff[0]).get_leaf(1) is staff[1]
    assert abjad.inspect(staff[1]).get_leaf(1) is staff[2]
    assert abjad.inspect(staff[2]).get_leaf(1) is staff[3]
    assert abjad.inspect(staff[3]).get_leaf(1) is None

    assert abjad.inspect(staff[0]).get_leaf(-1) is None
    assert abjad.inspect(staff[1]).get_leaf(-1) is staff[0]
    assert abjad.inspect(staff[2]).get_leaf(-1) is staff[1]
    assert abjad.inspect(staff[3]).get_leaf(-1) is staff[2]

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8
            cs'8
            d'8
            ef'8
        }
        '''
        )


def test_scoretools_Inspection_get_leaf_04():
    r'''Container.
    '''

    container = abjad.Container([abjad.Note(i, (1, 8)) for i in range(4)])

    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'8
            cs'8
            d'8
            ef'8
        }
        '''
        )

    assert abjad.inspect(container[0]).get_leaf(1) is container[1]
    assert abjad.inspect(container[1]).get_leaf(1) is container[2]
    assert abjad.inspect(container[2]).get_leaf(1) is container[3]
    assert abjad.inspect(container[3]).get_leaf(1) is None

    assert abjad.inspect(container[0]).get_leaf(-1) is None
    assert abjad.inspect(container[1]).get_leaf(-1) is container[0]
    assert abjad.inspect(container[2]).get_leaf(-1) is container[1]
    assert abjad.inspect(container[3]).get_leaf(-1) is container[2]


def test_scoretools_Inspection_get_leaf_05():
    r'''Tuplet.
    '''

    tuplet = abjad.Tuplet((2, 3), "c'8 cs'8 d'8")

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \times 2/3 {
            c'8
            cs'8
            d'8
        }
        '''
        )

    assert abjad.inspect(tuplet[0]).get_leaf(1) is tuplet[1]
    assert abjad.inspect(tuplet[1]).get_leaf(1) is tuplet[2]
    assert abjad.inspect(tuplet[2]).get_leaf(1) is None

    assert abjad.inspect(tuplet[0]).get_leaf(-1) is None
    assert abjad.inspect(tuplet[1]).get_leaf(-1) is tuplet[0]
    assert abjad.inspect(tuplet[2]).get_leaf(-1) is tuplet[1]


def test_scoretools_Inspection_get_leaf_06():
    r'''Contiguous containers inside a voice.
    '''

    container_1 = abjad.Container([abjad.Note(i, (1, 8)) for i in range(4)])
    container_2 = abjad.Container([abjad.Note(i, (1, 8)) for i in range(4, 8)])
    voice = abjad.Voice([container_1, container_2])

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(container_1[0]).get_leaf(1) is container_1[1]
    assert abjad.inspect(container_1[1]).get_leaf(1) is container_1[2]
    assert abjad.inspect(container_1[2]).get_leaf(1) is container_1[3]
    assert abjad.inspect(container_1[3]).get_leaf(1) is container_2[0]

    assert abjad.inspect(container_1[1]).get_leaf(-1) is container_1[0]
    assert abjad.inspect(container_1[2]).get_leaf(-1) is container_1[1]
    assert abjad.inspect(container_1[3]).get_leaf(-1) is container_1[2]
    assert abjad.inspect(container_2[0]).get_leaf(-1) is container_1[3]


def test_scoretools_Inspection_get_leaf_07():
    r'''Tuplets inside a voice.
    '''

    tuplet_1 = abjad.Tuplet((2, 3), "c'8 cs'8 d'8")
    tuplet_2 = abjad.Tuplet((2, 3), "ef'8 e'8 f'8")
    voice = abjad.Voice([tuplet_1, tuplet_2])

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(tuplet_1[0]).get_leaf(1) is tuplet_1[1]
    assert abjad.inspect(tuplet_1[1]).get_leaf(1) is tuplet_1[2]
    assert abjad.inspect(tuplet_1[2]).get_leaf(1) is tuplet_2[0]

    assert abjad.inspect(tuplet_1[1]).get_leaf(-1) is tuplet_1[0]
    assert abjad.inspect(tuplet_1[2]).get_leaf(-1) is tuplet_1[1]
    assert abjad.inspect(tuplet_2[0]).get_leaf(-1) is tuplet_1[2]


def test_scoretools_Inspection_get_leaf_08():
    r'''Does not continue across contiguous anonymous voices inside a staff.
    '''

    voice_1 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4)])
    voice_2 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4, 8)])
    staff = abjad.Staff([voice_1, voice_2])

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(voice_1[3]).get_leaf(1) is None
    assert abjad.inspect(voice_2[0]).get_leaf(-1) is None


def test_scoretools_Inspection_get_leaf_09():
    r'''Does cross contiguous equally named voices inside a staff.
    '''

    voice_1 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4)])
    voice_1.name = 'My Voice'
    voice_2 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4, 8)])
    voice_2.name = 'My Voice'
    staff = abjad.Staff([voice_1, voice_2])

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(voice_1[0]).get_leaf(1) is voice_1[1]
    assert abjad.inspect(voice_1[1]).get_leaf(1) is voice_1[2]
    assert abjad.inspect(voice_1[2]).get_leaf(1) is voice_1[3]
    assert abjad.inspect(voice_1[3]).get_leaf(1) is voice_2[0]

    assert abjad.inspect(voice_1[1]).get_leaf(-1) is voice_1[0]
    assert abjad.inspect(voice_1[2]).get_leaf(-1) is voice_1[1]
    assert abjad.inspect(voice_1[3]).get_leaf(-1) is voice_1[2]
    assert abjad.inspect(voice_2[0]).get_leaf(-1) is voice_1[3]


def test_scoretools_Inspection_get_leaf_10():
    r'''Does not connect through contiguous unequally named voices.
    '''

    voice_1 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4)])
    voice_1.name = 'Your Voice'
    voice_2 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4, 8)])
    voice_2.name = 'My Voice'
    staff = abjad.Staff([voice_1, voice_2])

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(voice_1[0]).get_leaf(1) is voice_1[1]
    assert abjad.inspect(voice_1[1]).get_leaf(1) is voice_1[2]
    assert abjad.inspect(voice_1[2]).get_leaf(1) is voice_1[3]
    assert abjad.inspect(voice_1[3]).get_leaf(1) is None

    voice_2.name = None
    assert abjad.inspect(voice_1[3]).get_leaf(1) is None

    assert abjad.inspect(voice_2[1]).get_leaf(-1) is voice_2[0]
    assert abjad.inspect(voice_2[2]).get_leaf(-1) is voice_2[1]
    assert abjad.inspect(voice_2[3]).get_leaf(-1) is voice_2[2]
    assert abjad.inspect(voice_2[0]).get_leaf(-1) is None


def test_scoretools_Inspection_get_leaf_11():
    r'''Does connect through like-named staves
    containing like-named voices.
    '''

    voice_1 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4)])
    voice_1.name = 'low'
    voice_2 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4, 8)])
    voice_2.name = 'low'

    staff_1 = abjad.Staff([voice_1])
    staff_1.name = 'mystaff'
    staff_2 = abjad.Staff([voice_2])
    staff_2.name = 'mystaff'

    container = abjad.Container([staff_1, staff_2])

    assert format(container) == abjad.String.normalize(
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

    assert abjad.inspect(voice_1[3]).get_leaf(1) is voice_2[0]
    assert abjad.inspect(voice_2[0]).get_leaf(-1) is voice_1[3]


def test_scoretools_Inspection_get_leaf_12():
    r'''Does connect through like-named staves containing
    like-named voices.
    '''

    lower_voice_1 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4)])
    lower_voice_1.name = 'low'
    lower_voice_2 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4 ,8)])
    lower_voice_2.name = 'low'
    higher_voice_1 = abjad.Voice([abjad.Note(i, (1 ,8)) for i in range(12,16)])
    higher_voice_1.name = 'high'
    higher_voice_2 = abjad.Voice([abjad.Note(i, (1 ,8)) for i in range(16,20)])
    higher_voice_2.name = 'high'

    staff_1 = abjad.Staff([higher_voice_1, lower_voice_1])
    staff_1.name = 'mystaff'
    staff_1.is_simultaneous = True
    staff_2 = abjad.Staff([lower_voice_2, higher_voice_2])
    staff_2.name = 'mystaff'
    staff_2.is_simultaneous = True

    container = abjad.Container([staff_1, staff_2])

    assert format(container) == abjad.String.normalize(
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

    assert abjad.inspect(lower_voice_1[3]).get_leaf(1) is lower_voice_2[0]
    assert abjad.inspect(higher_voice_1[3]).get_leaf(1) is higher_voice_2[0]

    assert abjad.inspect(lower_voice_2[0]).get_leaf(-1) is lower_voice_1[3]
    assert abjad.inspect(higher_voice_2[0]).get_leaf(-1) is higher_voice_1[3]


def test_scoretools_Inspection_get_leaf_13():
    r'''Does connect through symmetrical nested containers in a voice.
    '''

    container_1 = abjad.Container([abjad.Note(i, (1 ,8)) for i in range(4)])
    container_1 = abjad.Container([container_1])
    container_2 = abjad.Container([abjad.Note(i, (1 ,8)) for i in range(4 ,8)])
    container_2 = abjad.Container([container_2])
    voice = abjad.Voice([container_1, container_2])

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(container_1[0][0]).get_leaf(1) is container_1[0][1]
    assert abjad.inspect(container_1[0][1]).get_leaf(1) is container_1[0][2]
    assert abjad.inspect(container_1[0][2]).get_leaf(1) is container_1[0][3]
    assert abjad.inspect(container_1[0][3]).get_leaf(1) is container_2[0][0]

    assert abjad.inspect(container_2[0][1]).get_leaf(-1) is container_2[0][0]
    assert abjad.inspect(container_2[0][2]).get_leaf(-1) is container_2[0][1]
    assert abjad.inspect(container_2[0][3]).get_leaf(-1) is container_2[0][2]
    assert abjad.inspect(container_2[0][0]).get_leaf(-1) is container_1[0][3]


def test_scoretools_Inspection_get_leaf_14():
    r'''Tautological parentage asymmetries result in symmetric (balanced)
    logical voice parentage.
    '''

    container_1 = abjad.Container([abjad.Note(i, (1 ,8)) for i in range(4)])
    container_2 = abjad.Container([abjad.Note(i, (1 ,8)) for i in range(4 ,8)])
    container_2 = abjad.Container([container_2])
    container_2 = abjad.Container([container_2])
    voice = abjad.Voice([container_1, container_2])

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(container_1[0]).get_leaf(1) is container_1[1]
    assert abjad.inspect(container_1[1]).get_leaf(1) is container_1[2]
    assert abjad.inspect(container_1[2]).get_leaf(1) is container_1[3]
    assert abjad.inspect(container_1[3]).get_leaf(1) is container_2[0][0][0]

    assert abjad.inspect(container_2[0][0][1]).get_leaf(-1) is container_2[0][0][0]
    assert abjad.inspect(container_2[0][0][2]).get_leaf(-1) is container_2[0][0][1]
    assert abjad.inspect(container_2[0][0][3]).get_leaf(-1) is container_2[0][0][2]
    assert abjad.inspect(container_2[0][0][0]).get_leaf(-1) is container_1[3]


def test_scoretools_Inspection_get_leaf_15():
    r'''Tautological parentage asymmetries result in symmetric (balanced)
    lgoical voice parentage.
    '''

    container_1 = abjad.Container([abjad.Note(i, (1 ,8)) for i in range(4)])
    container_1 = abjad.Container([container_1])
    container_1 = abjad.Container([container_1])
    container_2 = abjad.Container([abjad.Note(i, (1 ,8)) for i in range(4 ,8)])
    voice = abjad.Voice([container_1, container_2])

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(container_1[0][0][0]).get_leaf(1) is container_1[0][0][1]
    assert abjad.inspect(container_1[0][0][1]).get_leaf(1) is container_1[0][0][2]
    assert abjad.inspect(container_1[0][0][2]).get_leaf(1) is container_1[0][0][3]
    assert abjad.inspect(container_1[0][0][3]).get_leaf(1) is container_2[0]

    assert abjad.inspect(container_2[0]).get_leaf(-1) is container_1[0][0][3]
    assert abjad.inspect(container_2[1]).get_leaf(-1) is container_2[0]
    assert abjad.inspect(container_2[2]).get_leaf(-1) is container_2[1]
    assert abjad.inspect(container_2[3]).get_leaf(-1) is container_2[2]


def test_scoretools_Inspection_get_leaf_16():
    r'''Does connect in sequence of alternating containers and notes.
    '''

    container_1 = abjad.Container([abjad.Note(i, (1, 8)) for i in range(2)])
    container_2 = abjad.Container([abjad.Note(i, (1, 8)) for i in range(3, 5)])
    voice = abjad.Voice([container_1, abjad.Note(2, (1, 8)), container_2])

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(container_1[1]).get_leaf(1) is voice[1]
    assert abjad.inspect(voice[1]).get_leaf(1) is container_2[0]

    assert abjad.inspect(voice[1]).get_leaf(-1) is container_1[1]
    assert abjad.inspect(container_2[0]).get_leaf(-1) is voice[1]


def test_scoretools_Inspection_get_leaf_17():
    r'''Does connect in sequence of alternating tuplets and notes.
    '''

    notes = [abjad.Note(i, abjad.Duration(1, 8)) for i in range(3)]
    tuplet_1 = abjad.Tuplet((2, 3), notes)
    notes = [abjad.Note(i, abjad.Duration(1, 8)) for i in range(4, 7)]
    tuplet_2 = abjad.Tuplet((2, 3), notes)
    voice = abjad.Voice([tuplet_1, abjad.Note(3, (1, 8)), tuplet_2])

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(tuplet_1[-1]).get_leaf(1) is voice[1]
    assert abjad.inspect(voice[1]).get_leaf(1) is tuplet_2[0]

    assert abjad.inspect(voice[1]).get_leaf(-1) is tuplet_1[-1]
    assert abjad.inspect(tuplet_2[0]).get_leaf(-1) is voice[1]


def test_scoretools_Inspection_get_leaf_18():
    r'''Does connect through asymmetrically nested tuplets.
    '''

    inner_tuplet = abjad.Tuplet((2, 3), "c'8 c'8 c'8")
    contents = [abjad.Note("c'4"), inner_tuplet, abjad.Note("c'4")]
    tuplet = abjad.Tuplet((2, 3), contents)

    assert format(tuplet) == abjad.String.normalize(
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

    assert abjad.inspect(tuplet[0]).get_leaf(1) is inner_tuplet[0]
    assert abjad.inspect(inner_tuplet[-1]).get_leaf(1) is tuplet[-1]
    assert abjad.inspect(tuplet[-1]).get_leaf(-1) is inner_tuplet[-1]
    assert abjad.inspect(inner_tuplet[0]).get_leaf(-1) is tuplet[0]


def test_scoretools_Inspection_get_leaf_19():
    r'''Returns none in asymmetric logical voice parentage structures.
    '''

    voice_1 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(3)])
    note = abjad.Note(3, (1, 8))
    voice_2 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4, 8)])
    staff = abjad.Staff([voice_1, note, voice_2])

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(voice_1[-1]).get_leaf(1) is None
    assert abjad.inspect(note).get_leaf(1) is None

    assert abjad.inspect(voice_2[0]).get_leaf(-1) is None
    assert abjad.inspect(note).get_leaf(-1) is None


def test_scoretools_Inspection_get_leaf_20():
    r'''Noncontiguous or broken logical voices do not connect.
    '''

    voice_1 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(3)])
    voice_1.name = 'My Voice'
    voice_2 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4, 8)])
    voice_2.name = 'Your Voice'
    voice_3 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(4, 8)])
    voice_3.name = 'My Voice'
    staff = abjad.Staff([voice_1, voice_2, voice_3])

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(voice_1[-1]).get_leaf(1) is None
    assert abjad.inspect(voice_2[-1]).get_leaf(1) is None

    voice_2.name = None

    assert abjad.inspect(voice_1[-1]).get_leaf(1) is None
    assert abjad.inspect(voice_2[-1]).get_leaf(1) is None

    assert abjad.inspect(voice_3[0]).get_leaf(-1) is None
    assert abjad.inspect(voice_2[0]).get_leaf(-1) is None


def test_scoretools_Inspection_get_leaf_21():
    r'''Does not connect through nested anonymous voices.
    '''

    inner_voice = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(3)])
    outer_voice = abjad.Voice([inner_voice, abjad.Note(3, (1, 8))])

    assert format(outer_voice) == abjad.String.normalize(
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

    assert abjad.inspect(inner_voice[0]).get_leaf(1) is inner_voice[1]
    assert abjad.inspect(inner_voice[1]).get_leaf(1) is inner_voice[2]
    assert abjad.inspect(inner_voice[2]).get_leaf(1) is None

    assert abjad.inspect(inner_voice[1]).get_leaf(-1) is inner_voice[0]
    assert abjad.inspect(inner_voice[2]).get_leaf(-1) is inner_voice[1]
    assert abjad.inspect(outer_voice[1]).get_leaf(-1) is None


def test_scoretools_Inspection_get_leaf_22():
    r'''Does not connect through nested anonymous voices.
    '''

    inner_voice = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(1, 4)])
    outer_voice = abjad.Voice([abjad.Note(0, (1, 8)), inner_voice])

    assert format(outer_voice) == abjad.String.normalize(
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

    assert abjad.inspect(inner_voice[0]).get_leaf(1) is inner_voice[1]
    assert abjad.inspect(inner_voice[1]).get_leaf(1) is inner_voice[2]
    assert abjad.inspect(outer_voice[0]).get_leaf(1) is None

    assert abjad.inspect(inner_voice[1]).get_leaf(-1) is inner_voice[0]
    assert abjad.inspect(inner_voice[2]).get_leaf(-1) is inner_voice[1]
    assert abjad.inspect(inner_voice[0]).get_leaf(-1) is None



def test_scoretools_Inspection_get_leaf_23():
    r'''Does connect through nested equally named voices.
    '''

    inner_voice = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(3)])
    inner_voice.name = 'My Voice'
    outer_voice = abjad.Voice([inner_voice, abjad.Note(3, (1, 8))])
    outer_voice.name = 'My Voice'

    assert format(outer_voice) == abjad.String.normalize(
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

    assert abjad.inspect(inner_voice[0]).get_leaf(1) is inner_voice[1]
    assert abjad.inspect(inner_voice[1]).get_leaf(1) is inner_voice[2]
    assert abjad.inspect(inner_voice[2]).get_leaf(1) is outer_voice[1]

    assert abjad.inspect(inner_voice[1]).get_leaf(-1) is inner_voice[0]
    assert abjad.inspect(inner_voice[2]).get_leaf(-1) is inner_voice[1]
    assert abjad.inspect(outer_voice[1]).get_leaf(-1) is inner_voice[-1]


def test_scoretools_Inspection_get_leaf_24():
    r'''Does connect through nested equally named voices.
    '''

    inner_voice = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(1, 4)])
    inner_voice.name = 'My Voice'
    outer_voice = abjad.Voice([abjad.Note(0, (1, 8)), inner_voice])
    outer_voice.name = 'My Voice'

    assert format(outer_voice) == abjad.String.normalize(
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

    assert abjad.inspect(inner_voice[0]).get_leaf(1) is inner_voice[1]
    assert abjad.inspect(inner_voice[1]).get_leaf(1) is inner_voice[2]
    assert abjad.inspect(outer_voice[0]).get_leaf(1) is inner_voice[0]

    assert abjad.inspect(inner_voice[1]).get_leaf(-1) is inner_voice[0]
    assert abjad.inspect(inner_voice[2]).get_leaf(-1) is inner_voice[1]
    assert abjad.inspect(inner_voice[0]).get_leaf(-1) is outer_voice[0]


def test_scoretools_Inspection_get_leaf_25():
    r'''Returns none on nested differently named voices.
    '''

    inner_voice = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(3)])
    inner_voice.name = 'Your Voice'
    outer_voice = abjad.Voice([inner_voice, abjad.Note(3, (1, 8))])
    outer_voice.name = 'My Voice'

    assert format(outer_voice) == abjad.String.normalize(
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

    assert abjad.inspect(inner_voice[0]).get_leaf(1) is inner_voice[1]
    assert abjad.inspect(inner_voice[1]).get_leaf(1) is inner_voice[2]
    assert abjad.inspect(inner_voice[2]).get_leaf(1) is None

    assert abjad.inspect(inner_voice[1]).get_leaf(-1) is inner_voice[0]
    assert abjad.inspect(inner_voice[2]).get_leaf(-1) is inner_voice[1]
    assert abjad.inspect(outer_voice[1]).get_leaf(-1) is None


def test_scoretools_Inspection_get_leaf_26():
    r'''Returns none on nested differently named voices.
    '''

    voice_2 = abjad.Voice([abjad.Note(i, (1, 8)) for i in range(1, 4)])
    voice_2.name = 'Voice 2'
    voice_1 = abjad.Voice([abjad.Note(0, (1, 8)), voice_2])
    voice_1.name = 'Voice 1'

    assert format(voice_1) == abjad.String.normalize(
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

    assert abjad.inspect(voice_2[0]).get_leaf(1) is voice_2[1]
    assert abjad.inspect(voice_2[1]).get_leaf(1) is voice_2[2]
    assert abjad.inspect(voice_1[0]).get_leaf(1) is None

    assert abjad.inspect(voice_2[1]).get_leaf(-1) is voice_2[0]
    assert abjad.inspect(voice_2[2]).get_leaf(-1) is voice_2[1]
    assert abjad.inspect(voice_1[1]).get_leaf(-1) is voice_2[-1]
