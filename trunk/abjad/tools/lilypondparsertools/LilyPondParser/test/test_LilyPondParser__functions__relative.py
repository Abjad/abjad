import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__functions__relative_01():
    pitches = [2, 5, 9, 7, 12, 11, 5, 2]
    target = Container(notetools.make_notes(pitches, (1, 4)))

    r'''{
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

    input = r"\relative c' { d f a g c b f d }"
    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result


def test_LilyPondParser__functions__relative_02():
    pitches = [11, 12, 11, 14, 11, 16, 11, 9, 11, 7, 11, 5]
    target = Container(notetools.make_notes(pitches, (1, 4)))

    r'''{
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

    input = r"\relative c'' { b c b d b e b a b g b f }"
    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result


def test_LilyPondParser__functions__relative_03():
    pitches = [9, -3, 12, 5, 7, 31, 9, 17]
    target = Container(notetools.make_notes(pitches, (1, 4)))

    r"""{
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

    input = r"\relative c'' { a a, c' f, g g'' a,, f' }"
    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result


def test_LilyPondParser__functions__relative_04():
    pitches = [["a'", "c''", "e''"], ["f'", "a'", "c''"], ["a'", "c''", "e''"], ["f''", "a''", "c'''"], ["b", "b'", "e''"]]
    target = Container(leaftools.make_leaves(pitches, 1))

    r"""{
        <a' c'' e''>1
        <f' a' c''>1
        <a' c'' e''>1
        <f'' a'' c'''>1
        <b b' e''>1
    }
    """

    input = r'''\relative c'' { <a c e>1 <f a c> <a c e> <f' a c> <b, e b,> }'''
    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result


def test_LilyPondParser__functions__relative_05():
    pitches = ["c", "f", "b", "e'", "a'", "d''", "g''", "c'''"]
    target = Container(notetools.make_notes(pitches, [(1, 4)]))

    r"""{
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

    input = r'''\relative c { c f b e a d g c }'''
    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result


def test_LilyPondParser__functions__relative_06():
    py.test.skip()
    # \relative { <c e g> b c q } etc.

    pitches = [["c'", "e'", "g'"], "fs'", ]

    target = None

    input = r''''''
    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result


def test_LilyPondParser__functions__relative_07():
    target = Container([
        Note("c'", (1, 4)), Note("d'", (1, 4)), Note("e'", (1, 4)), Note("f'", (1, 4)), Container([
            Note("c''", (1, 4)), Note("d''", (1, 4)), Note("e''", (1, 4)), Note("f''", (1, 4)),
        ])
    ])

    r'''{
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

    input = r'''\relative c' { c d e f \relative c'' { c d e f } }'''
    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result


def test_LilyPondParser__functions__relative_08():
    target = Container([
        Note("d'", (1, 4)), Note("e'", (1, 4)), Container([
            Note("e", (1, 4)), Note("fs", (1, 4)), Container([
                Note("e'", (1, 4)), Note("fs'", (1, 4))
            ])
        ])
    ])

    r'''{
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

    input = r'''\relative c' { d e \transpose f g { d e \relative c' { d e } } }'''
    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result


def test_LilyPondParser__functions__relative_09():
    target = Container([
        Note("c'", (1, 4)),
        Chord(["c'", "e'", "g'"], (1, 4)),
        Chord(["c''", "e''", "g'''"], (1, 4)),
        Chord(["e", "c'", "g''"], (1, 4)),
    ])

    r"""{
        c'4
        <c' e' g'>4
        <c'' e'' g'''>4
        <e c' g''>4
    }
    """

    input = r'''\relative c' { c <c e g> <c' e g'> <c, e, g''> }'''
    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result


def test_LilyPondParser__functions__relative_10():
    # py.test.skip('Abjad cannot yet diatonically transpose double-sharp or double-flat pitches.')
    # http://lilypond.org/doc/v2.15/Documentation/c6/lily-8d84e2b9.ly
    pitches = ["c''", "fs''", "c''", "gf'", "b'", "ess''", "b'", "fff'"]
    target = Container(notetools.make_notes(pitches, [(1, 2)]))

    r'''{
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

    input = r'''\relative c'' { c2 fs c2 gf b2 ess b2 fff }'''
    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result
