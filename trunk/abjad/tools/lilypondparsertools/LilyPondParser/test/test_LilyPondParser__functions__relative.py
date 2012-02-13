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


def test_LilyPondParser__function__relative_02():
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


def test_LilyPondParser__function__relative_03():
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


def test_LilyPondParser__function__relative_04():
    pitches = [["a'", "c''", "e''"], ["f'", "a'", "c''"], ["a'", "c''", "e''"], ["f''", "a''", "c'''"], ["b", "b'", "e''"]]
    target = Container(leaftools.make_leaves(pitches, 1))

    # from http://lilypond.org/doc/v2.14/Documentation/b0/lily-b788d67f.ly
    # notes in a chord are relative the first note of that chord
    # the first note of a chord is relative the bottom note of the previous chord

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
