import abjad


def test_scoretools_Selection_are_logical_voice_01():
    r'''Unincorporated leaves do not share a logical voice.
    Unicorporated leaves do not share a root component.
    False if not allow orphans; True if allow orphans.
    '''

    notes = [
        abjad.Note("c'8"),
        abjad.Note("d'8"), abjad.Note("e'8"), abjad.Note("f'8")]
    assert abjad.select(notes).are_logical_voice()
    assert not abjad.select(notes).are_logical_voice(allow_orphans=False)


def test_scoretools_Selection_are_logical_voice_02():
    r'''Container and leaves all logical voice.
    '''

    container = abjad.Container("c'8 d'8 e'8 f'8")

    r'''
    {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert abjad.select(container).components().are_logical_voice()


def test_scoretools_Selection_are_logical_voice_03():
    r'''Tuplet and leaves all logical voice.
    '''

    tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")

    r'''
    \times 2/3 {
        c'8
        d'8
        e'8
    }
    '''

    assert abjad.select(tuplet).components().are_logical_voice()


def test_scoretools_Selection_are_logical_voice_04():
    r'''Voice and leaves all appear in same logical voice.
    '''

    voice = abjad.Voice("c'8 d'8 e'8 f'8")

    r'''
    \new Voice {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert abjad.select(voice).components().are_logical_voice()


def test_scoretools_Selection_are_logical_voice_05():
    r'''Anonymous staff and leaves all appear in same logical voice.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8")

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert abjad.select(staff).components().are_logical_voice()


def test_scoretools_Selection_are_logical_voice_06():
    r'''Voice, sequential and leaves all appear in same logical voice.
    '''

    voice = abjad.Voice(r'''
        {
            c'8
            d'8
            e'8
            f'8
        }
        {
            g'8
            a'8
            b'8
            c''8
        }
        ''')

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            {
                c'8
                d'8
                e'8
                f'8
            }
            {
                g'8
                a'8
                b'8
                c''8
            }
        }
        '''
        )

    assert abjad.select(voice).components().are_logical_voice()


def test_scoretools_Selection_are_logical_voice_07():
    r'''Anonymous voice, tuplets and leaves all appear in same logical voice.
    '''

    voice = abjad.Voice(r'''
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        \times 2/3 {
            f'8
            g'8
            a'8
        }
        ''')

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            \times 2/3 {
                f'8
                g'8
                a'8
            }
        }
        '''
        )

    assert abjad.select(voice).components().are_logical_voice()


def test_scoretools_Selection_are_logical_voice_08():
    r'''Logical voice does not extend across anonymous voices.
    '''

    staff = abjad.Staff(r'''
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
        ''')

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
    assert leaves[:4].are_logical_voice()
    assert leaves[4:].are_logical_voice()
    assert not leaves.are_logical_voice()
    assert not staff[:].are_logical_voice()


def test_scoretools_Selection_are_logical_voice_09():
    r'''Logical voice encompasses across like-named voices.
    '''

    staff = abjad.Staff(r'''
        \context Voice = "foo" {
            c'8
            d'8
            e'8
            f'8
        }
        \context Voice = "foo" {
            g'8
            a'8
            b'8
            c''8
        }
        ''')

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \context Voice = "foo" {
                c'8
                d'8
                e'8
                f'8
            }
            \context Voice = "foo" {
                g'8
                a'8
                b'8
                c''8
            }
        }
        '''
        )

    leaves = abjad.select(staff).leaves()
    assert leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_10():
    r'''Logical voice does not extend across differently named voices.
    '''

    staff = abjad.Staff(r'''
        \context Voice = "foo" {
            c'8
            d'8
        }
        \context Voice = "bar" {
            e'8
            f'8
        }
        ''')

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \context Voice = "foo" {
                c'8
                d'8
            }
            \context Voice = "bar" {
                e'8
                f'8
            }
        }
        '''
        )

    leaves = abjad.select(staff).leaves()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_11():
    r'''Logical voice does not across anonymous voices.
    Logical voice does not extend across anonymous staves.
    '''

    container = abjad.Container(r'''
        \new Staff {
            \new Voice {
                c'8
                d'8
            }
        }
        \new Staff {
            \new Voice {
                e'8
                f'8
            }
        }
        ''')

    assert format(container) == abjad.String.normalize(
        r'''
        {
            \new Staff {
                \new Voice {
                    c'8
                    d'8
                }
            }
            \new Staff {
                \new Voice {
                    e'8
                    f'8
                }
            }
        }
        '''
        )

    leaves = abjad.select(container).leaves()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_12():
    r'''Logical voice does not extend across anonymous voices.
    Logical voice does not extend across anonymous staves.
    '''

    container = abjad.Container(r'''
        \new Staff <<
            \new Voice {
                c'8
                d'8
            }
            \new Voice {
                e'8
                f'8
            }
        >>
        \new Staff <<
            \new Voice {
                g'8
                a'8
            }
            \new Voice {
                b'8
                c''8
            }
        >>
        ''')

    assert format(container) == abjad.String.normalize(
        r'''
        {
            \new Staff <<
                \new Voice {
                    c'8
                    d'8
                }
                \new Voice {
                    e'8
                    f'8
                }
            >>
            \new Staff <<
                \new Voice {
                    g'8
                    a'8
                }
                \new Voice {
                    b'8
                    c''8
                }
            >>
        }
        '''
        )

    leaves = abjad.select(container).leaves()
    assert not leaves[:4].are_logical_voice()


def test_scoretools_Selection_are_logical_voice_13():
    r'''Anonymous voice, sequentials and leaves all appear in same
    logical voice.
    '''

    voice = abjad.Voice(r'''
        {
            c'8
            d'8
        }
        {
            e'8
            f'8
        }
        ''')

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            {
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
        }
        '''
        )

    leaves = abjad.select(voice).leaves()
    assert leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_14():
    r'''Logical voice can extend across like-named staves.
    Logical voice can not extend across differently named implicit voices.
    '''

    container = abjad.Container(r'''
        \context Staff = "foo" {
            c'8
            cs'8
            d'8
            ef'8
        }
        \context Staff = "foo" {
            e'8
            f'8
            fs'8
            g'8
        }
        ''')

    assert format(container) == abjad.String.normalize(
        r'''
        {
            \context Staff = "foo" {
                c'8
                cs'8
                d'8
                ef'8
            }
            \context Staff = "foo" {
                e'8
                f'8
                fs'8
                g'8
            }
        }
        '''
        )

    leaves = abjad.select(container).leaves()
    assert leaves[:4].are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_15():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = abjad.Container(r'''
        {
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
        ''')

    assert format(container) == abjad.String.normalize(
        r'''
        {
            {
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

    leaves = abjad.select(container).leaves()
    assert leaves[:4].are_logical_voice()
    assert leaves[4:].are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_16():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = abjad.Container(r'''
        \new Voice {
            c'8
            d'8
            e'8
            f'8
        }
        {
            g'8
            a'8
            b'8
            c''8
        }
        ''')

    assert format(container) == abjad.String.normalize(
        r'''
        {
            \new Voice {
                c'8
                d'8
                e'8
                f'8
            }
            {
                g'8
                a'8
                b'8
                c''8
            }
        }
        '''
        )

    leaves = abjad.select(container).leaves()
    assert leaves[:4].are_logical_voice()
    assert leaves[4:].are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_17():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = abjad.Container(r'''
        {
            c'8
            d'8
            e'8
            f'8
        }
        \context Voice = "foo" {
            g'8
            a'8
            b'8
            c''8
        }
        ''')

    r'''
    {
        {
            c'8
            d'8
            e'8
            f'8
        }
        \context Voice = "foo" {
            g'8
            a'8
            b'8
            c''8
        }
    }
    '''

    leaves = abjad.select(container).leaves()
    assert leaves[:4].are_logical_voice()
    assert leaves[4:].are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_18():
    r'''Logical voice can not extend acrossdifferently named implicit voices.
    '''

    container = abjad.Container(r'''
        \context Voice = "foo" {
            c'8
            d'8
            e'8
            f'8
        }
        {
            g'8
            a'8
            b'8
            c''8
        }
        ''')

    assert format(container) == abjad.String.normalize(
        r'''
        {
            \context Voice = "foo" {
                c'8
                d'8
                e'8
                f'8
            }
            {
                g'8
                a'8
                b'8
                c''8
            }
        }
        '''
        )

    leaves = abjad.select(container).leaves()
    assert leaves[:4].are_logical_voice()
    assert leaves[4:].are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_19():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = abjad.Container(r'''
        {
            c'8
            d'8
            e'8
            f'8
        }
        \new Staff {
            g'8
            a'8
            b'8
            c''8
        }
        ''')

    assert format(container) == abjad.String.normalize(
        r'''
        {
            {
                c'8
                d'8
                e'8
                f'8
            }
            \new Staff {
                g'8
                a'8
                b'8
                c''8
            }
        }
        '''
        )

    leaves = abjad.select(container).leaves()
    assert leaves[:4].are_logical_voice()
    assert leaves[4:].are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_20():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = abjad.Container(r'''
        \new Staff {
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
        ''')

    assert format(container) == abjad.String.normalize(
        r'''
        {
            \new Staff {
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

    leaves = abjad.select(container).leaves()
    assert leaves[:4].are_logical_voice()
    assert leaves[4:].are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_21():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = abjad.Container(r'''
        c'8
        cs'8
        d'8
        ef'8
        \new Voice {
            e'8
            f'8
            fs'8
            g'8
        }
        ''')

    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'8
            cs'8
            d'8
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

    leaves = abjad.select(container).leaves()
    assert leaves[:4].are_logical_voice()
    assert leaves[4:].are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_22():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = abjad.Container(r'''
        \new Voice {
            c'8
            cs'8
            d'8
            ef'8
        }
        e'8
        f'8
        fs'8
        g'8
        ''')

    assert format(container) == abjad.String.normalize(
        r'''
        {
            \new Voice {
                c'8
                cs'8
                d'8
                ef'8
            }
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    leaves = abjad.select(container).leaves()
    assert leaves[:4].are_logical_voice()
    assert leaves[4:].are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_23():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = abjad.Container(r'''
        c'8
        cs'8
        d'8
        ef'8
        \context Voice = "foo" {
            e'8
            f'8
            fs'8
            g'8
        }
        ''')

    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'8
            cs'8
            d'8
            ef'8
            \context Voice = "foo" {
                e'8
                f'8
                fs'8
                g'8
            }
        }
        '''
        )

    leaves = abjad.select(container).leaves()
    assert leaves[:4].are_logical_voice()
    assert leaves[4:].are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_24():
    r'''Logical voice can not extend across differently named implicit voices.
    NOTE: THIS IS THE LILYPOND LACUNA.
    LilyPond *does* extend logical voice in this case.
    Abjad does not.
    '''

    container = abjad.Container(r'''
        \context Voice = "foo" {
            c'8
            cs'8
            d'8
            ef'8
        }
        e'8
        f'8
        fs'8
        g'8
        ''')

    assert format(container) == abjad.String.normalize(
        r'''
        {
            \context Voice = "foo" {
                c'8
                cs'8
                d'8
                ef'8
            }
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    leaves = abjad.select(container).leaves()
    assert leaves[:4].are_logical_voice()
    assert leaves[4:].are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_25():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = abjad.Container(r'''
        c'8
        cs'8
        d'8
        ef'8
        \new Voice {
            e'8
            f'8
            fs'8
            g'8
        }
        ''')

    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'8
            cs'8
            d'8
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

    leaves = abjad.select(container).leaves()
    assert leaves[:4].are_logical_voice()
    assert leaves[4:].are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_26():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = abjad.Container(r'''
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
        g'8
        a'8
        b'8
        c''8
        ''')

    assert format(container) == abjad.String.normalize(
        r'''
        {
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
            g'8
            a'8
            b'8
            c''8
        }
        '''
        )

    leaves = abjad.select(container).leaves()
    assert leaves[:4].are_logical_voice()
    assert leaves[4:].are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_27():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    voice = abjad.Voice([abjad.Note(n, (1, 8)) for n in range(4)])
    container = abjad.Container([voice])
    notes = [abjad.Note(n, (1, 8)) for n in range(4, 8)]
    container = abjad.Container([container] + notes)

    assert format(container) == abjad.String.normalize(
        r'''
        {
            {
                \new Voice {
                    c'8
                    cs'8
                    d'8
                    ef'8
                }
            }
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    leaves = abjad.select(container).leaves()
    assert leaves[:4].are_logical_voice()
    assert leaves[4:].are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_28():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    voice = abjad.Voice([abjad.Note(n, (1, 8)) for n in range(4)])
    voice.name = 'foo'
    container = abjad.Container([voice])
    notes = [abjad.Note(n, (1, 8)) for n in range(4, 8)]
    container = abjad.Container([container] + notes)

    r'''
    {
        {
            \context Voice = "foo" {
                c'8
                cs'8
                d'8
                ef'8
            }
        }
        e'8
        f'8
        fs'8
        g'8
    }
    '''

    leaves = abjad.select(container).leaves()
    assert leaves[:4].are_logical_voice()
    assert leaves[4:].are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_29():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    voice_1 = abjad.Voice([abjad.Note(n, (1, 8)) for n in range(4)])
    voice_1.name = 'foo'
    voice_2 = abjad.Voice([voice_1])
    voice_2.name = 'bar'
    notes = [abjad.Note(n, (1, 8)) for n in range(4, 8)]
    container = abjad.Container([voice_2] + notes)

    assert format(container) == abjad.String.normalize(
        r'''
        {
            \context Voice = "bar" {
                \context Voice = "foo" {
                    c'8
                    cs'8
                    d'8
                    ef'8
                }
            }
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    leaves = abjad.select(container).leaves()
    assert leaves[:4].are_logical_voice()
    assert leaves[4:].are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_30():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    voice_1 = abjad.Voice([abjad.Note(n, (1, 8)) for n in range(4)])
    voice_2 = abjad.Voice([voice_1])
    notes = [abjad.Note(n, (1, 8)) for n in range(4, 8)]
    container = abjad.Container([voice_2] + notes)

    assert format(container) == abjad.String.normalize(
        r'''
        {
            \new Voice {
                \new Voice {
                    c'8
                    cs'8
                    d'8
                    ef'8
                }
            }
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    leaves = abjad.select(container).leaves()
    assert leaves[:4].are_logical_voice()
    assert leaves[4:].are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_31():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    notes = [abjad.Note(n, (1, 8)) for n in range(4)]
    voice_1 = abjad.Voice(abjad.Note(12, (1, 8)) * 4)
    voice_2 = abjad.Voice(abjad.Note(0, (1, 8)) * 4)
    container = abjad.Container([voice_1, voice_2])
    container.is_simultaneous = True
    container = abjad.Container(notes + [container])

    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'8
            cs'8
            d'8
            ef'8
            <<
                \new Voice {
                    c''8
                    c''8
                    c''8
                    c''8
                }
                \new Voice {
                    c'8
                    c'8
                    c'8
                    c'8
                }
            >>
        }
        '''
        )

    leaves = abjad.select(container).leaves()
    assert not leaves[:8].are_logical_voice()
    assert not leaves[4:].are_logical_voice()


def test_scoretools_Selection_are_logical_voice_32():
    r'''Logical voice can not extend across differently named implicit voices.
    '''

    container = abjad.Container(r'''
        <<
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
        >>
        af'8
        a'8
        bf'8
        b'8
        ''')

    assert format(container) == abjad.String.normalize(
        r'''
        {
            <<
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
            >>
            af'8
            a'8
            bf'8
            b'8
        }
        '''
        )

    leaves = abjad.select(container).leaves()
    assert not leaves[:8].are_logical_voice()
    assert not leaves[4:].are_logical_voice()


def test_scoretools_Selection_are_logical_voice_33():
    r'''Logical voice does extend across gaps.
    Logical voice can not extend across differently named voices.
    '''

    container = abjad.Container(r'''
        c'8
        cs'8
        \new Voice {
            d'8
            ef'8
            \new Voice {
                e'8
                f'8
                fs'8
                g'8
            }
            af'8
            a'8
        }
        bf'8
        b'8
        ''')

    outer = (0, 1, 10, 11)
    middle = (2, 3, 8, 9)
    inner = (4, 5, 6, 7)

    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'8
            cs'8
            \new Voice {
                d'8
                ef'8
                \new Voice {
                    e'8
                    f'8
                    fs'8
                    g'8
                }
                af'8
                a'8
            }
            bf'8
            b'8
        }
        '''
        )

    leaves = abjad.select(container).leaves()
    assert abjad.select([leaves[i] for i in outer]).are_logical_voice()
    assert abjad.select([leaves[i] for i in middle]).are_logical_voice()
    assert abjad.select([leaves[i] for i in inner]).are_logical_voice()
    assert not leaves[:4].are_logical_voice()


def test_scoretools_Selection_are_logical_voice_34():
    r'''Logical voice does extend across gaps.
    Logical voice can not extend across differently named implicit voices.
    '''

    staff = abjad.Staff(r'''
        c'8
        cs'8
        \new Staff {
            d'8
            ef'8
            \new Staff {
                e'8
                f'8
                fs'8
                g'8
            }
            af'8
            a'8
        }
        bf'8
        b'8
        ''')

    outer = (0, 1, 10, 11)
    middle = (2, 3, 8, 9)
    inner = (4, 5, 6, 7)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8
            cs'8
            \new Staff {
                d'8
                ef'8
                \new Staff {
                    e'8
                    f'8
                    fs'8
                    g'8
                }
                af'8
                a'8
            }
            bf'8
            b'8
        }
        '''
        )

    leaves = abjad.select(staff).leaves()
    assert abjad.select([leaves[i] for i in outer]).are_logical_voice()
    assert abjad.select([leaves[i] for i in middle]).are_logical_voice()
    assert abjad.select([leaves[i] for i in inner]).are_logical_voice()
    assert not leaves[:4].are_logical_voice()


def test_scoretools_Selection_are_logical_voice_35():
    r'''Containers and leaves all appear in same logical voice.
    '''

    container = abjad.Container(r'''
        c'8
        cs'8
        {
            d'8
            ef'8
            {
                e'8
                f'8
                fs'8
                g'8
            }
            af'8
            a'8
        }
        bf'8
        b'8
        ''')

    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'8
            cs'8
            {
                d'8
                ef'8
                {
                    e'8
                    f'8
                    fs'8
                    g'8
                }
                af'8
                a'8
            }
            bf'8
            b'8
        }
        '''
        )

    assert abjad.select(container).components().are_logical_voice()


def test_scoretools_Selection_are_logical_voice_36():
    r'''Logical voice can not extend across differently named voices.
    '''

    container = abjad.Container(r'''
        c'8
        cs'8
        {
            {
                \context Voice = "foo" {
                    d'8
                    ef'8
                    e'8
                    f'8
                }
            }
        }
        fs'8
        g'8
        ''')

    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'8
            cs'8
            {
                {
                    \context Voice = "foo" {
                        d'8
                        ef'8
                        e'8
                        f'8
                    }
                }
            }
            fs'8
            g'8
        }
        '''
        )

    outer = (0, 1, 6, 7)
    inner = (2, 3, 4, 5)

    leaves = abjad.select(container).leaves()
    assert abjad.select([leaves[i] for i in outer]).are_logical_voice()
    assert abjad.select([leaves[i] for i in inner]).are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_37():
    r'''Logical voice does not extend over differently named voices.
    '''

    container = abjad.Container(r'''
        {
            {
                \context Voice = "foo" {
                    c'8
                    cs'8
                    d'8
                    ef'8
                }
            }
        }
        e'8
        f'8
        fs'8
        g'8
        ''')

    assert format(container) == abjad.String.normalize(
        r'''
        {
            {
                {
                    \context Voice = "foo" {
                        c'8
                        cs'8
                        d'8
                        ef'8
                    }
                }
            }
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    leaves = abjad.select(container).leaves()
    assert leaves[:4].are_logical_voice()
    assert leaves[4:].are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_38():
    r'''Can not nest across differently named implicit voices.
    '''

    container = abjad.Voice(
        r'''
        {
            {
                {
                    c'8
                    cs'8
                    \new Voice {
                        d'8
                        ef'8
                        e'8
                        f'8
                    }
                    fs'8
                    g'8
                }
            }
        }
        ''')

    assert format(container) == abjad.String.normalize(
        r'''
        \new Voice {
            {
                {
                    {
                        c'8
                        cs'8
                        \new Voice {
                            d'8
                            ef'8
                            e'8
                            f'8
                        }
                        fs'8
                        g'8
                    }
                }
            }
        }
        '''
        )

    outer = (0, 1, 6, 7)
    inner = (2, 3, 4, 5)

    leaves = abjad.select(container).leaves()
    assert abjad.select([leaves[i] for i in outer]).are_logical_voice()
    assert abjad.select([leaves[i] for i in inner]).are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_39():
    r'''Logical voice can not extend across differently named voices.
    '''

    voice = abjad.Voice(r'''
        c'8
        cs'8
        {
            d'8
            ef'8
            {
                e'8
                f'8
                \context Voice = "bar" {
                    fs'8
                    g'8
                    af'8
                    a'8
                }
                bf'8
                b'8
            }
            c''8
            cs''8
        }
        d''8
        ef''8
        ''')
    voice.name = 'foo'

    assert format(voice) == abjad.String.normalize(
        r'''
        \context Voice = "foo" {
            c'8
            cs'8
            {
                d'8
                ef'8
                {
                    e'8
                    f'8
                    \context Voice = "bar" {
                        fs'8
                        g'8
                        af'8
                        a'8
                    }
                    bf'8
                    b'8
                }
                c''8
                cs''8
            }
            d''8
            ef''8
        }
        '''
        )

    outer = (0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15)
    inner = (6, 7, 8, 9)

    leaves = abjad.select(voice).leaves()
    assert abjad.select([leaves[i] for i in outer]).are_logical_voice()
    assert abjad.select([leaves[i] for i in inner]).are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_40():
    r'''Logical voice can not extend across differently named anonymous voices.
    '''

    container = abjad.Container(r'''
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
        af'8
        a'8
        bf'8
        b'8
        ''')

    assert format(container) == abjad.String.normalize(
        r'''
        {
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
            af'8
            a'8
            bf'8
            b'8
        }
        '''
        )

    leaves = abjad.select(container).leaves()
    assert leaves[:4].are_logical_voice()
    assert leaves[4:8].are_logical_voice()
    assert leaves[8:].are_logical_voice()
    assert not leaves[:8].are_logical_voice()
    assert not leaves[4:].are_logical_voice()
    assert not leaves.are_logical_voice()


def test_scoretools_Selection_are_logical_voice_41():
    r'''Logical voice can not extend across differently named anonymous voices.
    '''

    container = abjad.Container(r'''
        c'8
        cs'8
        <<
            \new Voice {
                d'8
                ef'8
                e'8
                f'8
            }
            \new Voice {
                fs'8
                g'8
                af'8
                a'8
            }
        >>
        bf'8
        b'8
        ''')

    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'8
            cs'8
            <<
                \new Voice {
                    d'8
                    ef'8
                    e'8
                    f'8
                }
                \new Voice {
                    fs'8
                    g'8
                    af'8
                    a'8
                }
            >>
            bf'8
            b'8
        }
        '''
        )

    outer = (0, 1, 10, 11)

    leaves = abjad.select(container).leaves()
    assert abjad.select([leaves[i] for i in outer]).are_logical_voice()
    assert leaves[2:6].are_logical_voice()
    assert leaves[6:10].are_logical_voice()
    assert not leaves[:6].are_logical_voice()
    assert not leaves.are_logical_voice()
