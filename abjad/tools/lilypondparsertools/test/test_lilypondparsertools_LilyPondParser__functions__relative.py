# -*- coding: utf-8 -*-
import abjad


def test_lilypondparsertools_LilyPondParser__functions__relative_01():

    maker = abjad.NoteMaker()
    pitches = [2, 5, 9, 7, 12, 11, 5, 2]
    target = abjad.Container(maker(pitches, (1, 4)))

    assert format(target) == abjad.String.normalize(
        r'''
        {
            d'4
            f'4
            a'4
            g'4
            c''4
            b'4
            f'4
            d'4
        }
        '''
        )

    string = r"\relative c' { d f a g c b f d }"
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__functions__relative_02():

    maker = abjad.NoteMaker()
    pitches = [11, 12, 11, 14, 11, 16, 11, 9, 11, 7, 11, 5]
    target = abjad.Container(maker(pitches, (1, 4)))

    assert format(target) == abjad.String.normalize(
        r'''
        {
            b'4
            c''4
            b'4
            d''4
            b'4
            e''4
            b'4
            a'4
            b'4
            g'4
            b'4
            f'4
        }
        '''
        )

    string = r"\relative c'' { b c b d b e b a b g b f }"
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__functions__relative_03():

    pitches = [9, -3, 12, 5, 7, 31, 9, 17]
    maker = abjad.NoteMaker()
    target = abjad.Container(maker(pitches, (1, 4)))

    assert format(target) == abjad.String.normalize(
        r"""
        {
            a'4
            a4
            c''4
            f'4
            g'4
            g'''4
            a'4
            f''4
        }
        """
        )

    string = r"\relative c'' { a a, c' f, g g'' a,, f' }"
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__functions__relative_04():

    maker = abjad.LeafMaker()
    pitches = [["a'", "c''", "e''"], ["f'", "a'", "c''"], ["a'", "c''", "e''"], ["f''", "a''", "c'''"], ["b", "b'", "e''"]]
    leaves = maker(pitches, 1)
    target = abjad.Container(leaves)

    assert format(target) == abjad.String.normalize(
        r"""
        {
            <a' c'' e''>1
            <f' a' c''>1
            <a' c'' e''>1
            <f'' a'' c'''>1
            <b b' e''>1
        }
        """
        )

    string = r'''\relative c'' { <a c e>1 <f a c> <a c e> <f' a c> <b, e b,> }'''
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__functions__relative_05():

    pitches = ["c", "f", "b", "e'", "a'", "d''", "g''", "c'''"]
    maker = abjad.NoteMaker()
    target = abjad.Container(maker(pitches, [(1, 4)]))

    assert format(target) == abjad.String.normalize(
        r"""
        {
            c4
            f4
            b4
            e'4
            a'4
            d''4
            g''4
            c'''4
        }
        """
        )

    string = r'''\relative c { c f b e a d g c }'''
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__functions__relative_06():

    target = abjad.Container([
        abjad.Note("c'", (1, 4)), abjad.Note("d'", (1, 4)), abjad.Note("e'", (1, 4)), abjad.Note("f'", (1, 4)), abjad.Container([
            abjad.Note("c''", (1, 4)), abjad.Note("d''", (1, 4)), abjad.Note("e''", (1, 4)), abjad.Note("f''", (1, 4)),
        ])
    ])

    assert format(target) == abjad.String.normalize(
        r'''
        {
            c'4
            d'4
            e'4
            f'4
            {
                c''4
                d''4
                e''4
                f''4
            }
        }
        '''
        )

    string = r'''\relative c' { c d e f \relative c'' { c d e f } }'''
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__functions__relative_07():

    target = abjad.Container([
        abjad.Note("d'", (1, 4)), abjad.Note("e'", (1, 4)), abjad.Container([
            abjad.Note("e", (1, 4)), abjad.Note("fs", (1, 4)), abjad.Container([
                abjad.Note("e'", (1, 4)), abjad.Note("fs'", (1, 4))
            ])
        ])
    ])

    assert format(target) == abjad.String.normalize(
        r'''
        {
            d'4
            e'4
            {
                e4
                fs4
                {
                    e'4
                    fs'4
                }
            }
        }
        '''
        )

    string = r'''\relative c' { d e \transpose f g { d e \relative c' { d e } } }'''
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__functions__relative_08():

    target = abjad.Container([
        abjad.Note("c'", (1, 4)),
        abjad.Chord(["c'", "e'", "g'"], (1, 4)),
        abjad.Chord(["c''", "e''", "g'''"], (1, 4)),
        abjad.Chord(["e", "c'", "g''"], (1, 4)),
    ])

    assert format(target) == abjad.String.normalize(
        r"""
        {
            c'4
            <c' e' g'>4
            <c'' e'' g'''>4
            <e c' g''>4
        }
        """
        )

    string = r'''\relative c' { c <c e g> <c' e g'> <c, e, g''> }'''
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__functions__relative_09():

    # http://lilypond.org/doc/v2.15/Documentation/c6/lily-8d84e2b9.ly
    pitches = ["c''", "fs''", "c''", "gf'", "b'", "ess''", "b'", "fff'"]
    maker = abjad.NoteMaker()
    target = abjad.Container(maker(pitches, [(1, 2)]))

    assert format(target) == abjad.String.normalize(
        r'''
        {
            c''2
            fs''2
            c''2
            gf'2
            b'2
            ess''2
            b'2
            fff'2
        }
        '''
        )

    string = r'''\relative c'' { c2 fs c2 gf b2 ess b2 fff }'''
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result
