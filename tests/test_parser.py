import pytest

import abjad


def test_LilyPondParser__comments_01():
    target = abjad.Container([abjad.Note(0, (1, 4))])

    string = r"""
    { c'4 }
    % { d'4 }
    % { e'4 }"""  # NOTE: no newline should follow the final brace

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result)


def test_LilyPondParser__containers__Container_01():
    parser = abjad.parser.LilyPondParser()
    target = abjad.Container()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__containers__Tuplet_01():
    notes = abjad.makers.make_notes([0, 2, 4], (1, 8))
    target = abjad.Tuplet((2, 3), notes)

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \tuplet 3/2
        {
            c'8
            d'8
            e'8
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__containers__nesting_01():
    target = abjad.Container(
        [abjad.Container([]), abjad.Container([abjad.Container([])])]
    )

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            {
            }
            {
                {
                }
            }
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__containers__simultaneous_01():
    target = abjad.Container()
    target.simultaneous = True
    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__contexts__PianoStaff_01():
    target = abjad.StaffGroup(
        [
            abjad.Staff(abjad.makers.make_notes([0, 2, 4, 5, 7], (1, 8))),
            abjad.Staff(abjad.makers.make_notes([0, 2, 4, 5, 7], (1, 8))),
        ]
    )
    target.lilypond_type = "PianoStaff"

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new PianoStaff
        <<
            \new Staff
            {
                c'8
                d'8
                e'8
                f'8
                g'8
            }
            \new Staff
            {
                c'8
                d'8
                e'8
                f'8
                g'8
            }
        >>
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__contexts__Score_01():
    target = abjad.Score()

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Score
        <<
        >>
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__contexts__Staff_01():
    target = abjad.Staff([])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__contexts__Staff_02():
    target = abjad.Staff([])
    target.simultaneous = True
    target.append(
        abjad.Voice(abjad.makers.make_notes([0, 2, 4, 5, 7, 9, 11, 12], (1, 8)))
    )
    target.append(
        abjad.Voice(abjad.makers.make_notes([0, 2, 4, 5, 7, 9, 11, 12], (1, 8)))
    )

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        <<
            \new Voice
            {
                c'8
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8
            }
            \new Voice
            {
                c'8
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8
            }
        >>
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__contexts__StaffGroup_01():
    target = abjad.StaffGroup([])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new StaffGroup
        <<
        >>
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__contexts__Voice_01():
    target = abjad.Voice([])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Voice
        {
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__contexts__context_ids_01():
    notes = abjad.makers.make_notes([0, 2, 4, 5, 7], (1, 8))
    target = abjad.Staff(notes)
    target.name = "foo"

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \context Staff = "foo"
        {
            c'8
            d'8
            e'8
            f'8
            g'8
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__contexts__with_blocks_01():
    target = abjad.Staff([])

    r"""
    \new Staff {
    }
    """

    string = r"""\new Staff \with { } {
    }
    """

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__functions__grace_01():
    target = abjad.Container([abjad.Note("c'4"), abjad.Note("d'4"), abjad.Note("e'2")])

    grace = abjad.BeforeGraceContainer([abjad.Note("g''16"), abjad.Note("fs''16")])

    abjad.attach(grace, target[2])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            c'4
            d'4
            \grace {
                g''16
                fs''16
            }
            e'2
        }
        """
    )

    string = r"{ c'4 d'4 \grace { g''16 fs''16} e'2 }"
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__functions__language_01():
    target = abjad.Container(
        [abjad.Note("cs'8"), abjad.Note("ds'8"), abjad.Note("ff'8")]
    )

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            cs'8
            ds'8
            ff'8
        }
        """
    )

    string = r"\language nederlands { cis'8 dis'8 fes'8 }"
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__functions__relative_01():
    pitches = [2, 5, 9, 7, 12, 11, 5, 2]
    notes = abjad.makers.make_notes(pitches, (1, 4))
    target = abjad.Container(notes)

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
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
        """
    )

    string = r"\relative c' { d f a g c b f d }"
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__functions__relative_02():
    pitches = [11, 12, 11, 14, 11, 16, 11, 9, 11, 7, 11, 5]
    notes = abjad.makers.make_notes(pitches, (1, 4))
    target = abjad.Container(notes)

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
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
        """
    )

    string = r"\relative c'' { b c b d b e b a b g b f }"
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__functions__relative_03():
    pitches = [9, -3, 12, 5, 7, 31, 9, 17]
    notes = abjad.makers.make_notes(pitches, (1, 4))
    target = abjad.Container(notes)

    assert abjad.lilypond(target) == abjad.string.normalize(
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
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__functions__relative_04():
    pitches = [
        ["a'", "c''", "e''"],
        ["f'", "a'", "c''"],
        ["a'", "c''", "e''"],
        ["f''", "a''", "c'''"],
        ["b", "b'", "e''"],
    ]
    leaves = abjad.makers.make_leaves(pitches, 1)
    target = abjad.Container(leaves)

    assert abjad.lilypond(target) == abjad.string.normalize(
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

    string = r"""\relative c'' { <a c e>1 <f a c> <a c e> <f' a c> <b, e b,> }"""
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__functions__relative_05():
    pitches = ["c", "f", "b", "e'", "a'", "d''", "g''", "c'''"]
    leaves = abjad.makers.make_leaves(pitches, [(1, 4)])
    target = abjad.Container(leaves)

    assert abjad.lilypond(target) == abjad.string.normalize(
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

    string = r"""\relative c { c f b e a d g c }"""
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__functions__relative_06():
    target = abjad.Container(
        [
            abjad.Note("c'", (1, 4)),
            abjad.Note("d'", (1, 4)),
            abjad.Note("e'", (1, 4)),
            abjad.Note("f'", (1, 4)),
            abjad.Container(
                [
                    abjad.Note("c''", (1, 4)),
                    abjad.Note("d''", (1, 4)),
                    abjad.Note("e''", (1, 4)),
                    abjad.Note("f''", (1, 4)),
                ]
            ),
        ]
    )

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
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
        """
    )

    string = r"""\relative c' { c d e f \relative c'' { c d e f } }"""
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__functions__relative_07():
    target = abjad.Container(
        [
            abjad.Note("d'", (1, 4)),
            abjad.Note("e'", (1, 4)),
            abjad.Container(
                [
                    abjad.Note("e", (1, 4)),
                    abjad.Note("fs", (1, 4)),
                    abjad.Container(
                        [abjad.Note("e'", (1, 4)), abjad.Note("fs'", (1, 4))]
                    ),
                ]
            ),
        ]
    )

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
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
        """
    )

    string = r"""\relative c' { d e \transpose f g { d e \relative c' { d e } } }"""
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__functions__relative_08():
    target = abjad.Container(
        [
            abjad.Note("c'", (1, 4)),
            abjad.Chord(["c'", "e'", "g'"], (1, 4)),
            abjad.Chord(["c''", "e''", "g'''"], (1, 4)),
            abjad.Chord(["e", "c'", "g''"], (1, 4)),
        ]
    )

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            c'4
            <c' e' g'>4
            <c'' e'' g'''>4
            <e c' g''>4
        }
        """
    )

    string = r"""\relative c' { c <c e g> <c' e g'> <c, e, g''> }"""
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__functions__relative_09():
    # http://lilypond.org/doc/v2.15/Documentation/c6/lily-8d84e2b9.ly
    pitches = ["c''", "fs''", "c''", "gf'", "b'", "ess''", "b'", "fff'"]
    notes = abjad.makers.make_notes(pitches, [(1, 2)])
    target = abjad.Container(notes)

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
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
        """
    )

    string = r"""\relative c'' { c2 fs c2 gf b2 ess b2 fff }"""
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__functions__relative_10():
    pitches = ["c''", "bf''", "cf'''", "c'''", "cf'''", "c''", "cf''", "c''"]
    notes = abjad.makers.make_notes(pitches, [(1, 4)])
    target = abjad.Container(notes)

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            c''4
            bf''4
            cf'''4
            c'''4
            cf'''4
            c''4
            cf''4
            c''4
        }
        """
    )

    string = r"""\relative c'' { c bf' cf c cf c, cf c }"""
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__functions__relative_11():
    pitches = ["cs''", "b''", "bs''", "cs'''", "bs''", "cs''", "bs'", "cs''"]
    notes = abjad.makers.make_notes(pitches, [(1, 4)])
    target = abjad.Container(notes)

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            cs''4
            b''4
            bs''4
            cs'''4
            bs''4
            cs''4
            bs'4
            cs''4
        }
        """
    )

    string = r"""\relative cs'' { cs b' bs cs bs cs, bs cs }"""
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__functions__transpose_01():
    pitches = ["e'", "gs'", "b'", "e''"]
    target = abjad.Staff(abjad.makers.make_notes(pitches, (1, 4)))
    key_signature = abjad.KeySignature(abjad.NamedPitchClass("e"), abjad.Mode("major"))
    abjad.attach(key_signature, target[0])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \key e \major
            e'4
            gs'4
            b'4
            e''4
        }
        """
    )

    string = r"\transpose d e \relative c' \new Staff { \key d \major d4 fs a d }"
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__functions__transpose_02():
    pitches = ["ef'", "f'", "g'", "bf'"]
    target = abjad.Staff(abjad.makers.make_notes(pitches, (1, 4)))
    key_signature = abjad.KeySignature(abjad.NamedPitchClass("ef"), abjad.Mode("major"))
    abjad.attach(key_signature, target[0])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \key ef \major
            ef'4
            f'4
            g'4
            bf'4
        }
        """
    )

    string = r"\transpose a c' \relative c' \new Staff { \key c \major c4 d e g }"
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__functions__transpose_03():
    target = abjad.Staff(
        [
            abjad.Container(
                abjad.makers.make_notes(["cs'", "ds'", "es'", "fs'"], (1, 4))
            ),
            abjad.Container(
                abjad.makers.make_notes(["df'", "ef'", "f'", "gf'"], (1, 4))
            ),
        ]
    )

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
            {
                cs'4
                ds'4
                es'4
                fs'4
            }
            {
                df'4
                ef'4
                f'4
                gf'4
            }
        }
        """
    )

    string = r"""music = \relative c' { c d e f }
    \new Staff {
        \transpose c cs \music
        \transpose c df \music
    }
    """

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__indicators__Articulation_01():
    target = abjad.Staff(abjad.makers.make_notes(["c''"], [(1, 4)] * 6 + [(1, 2)]))
    articulation = abjad.Articulation("marcato")
    abjad.attach(articulation, target[0], direction=abjad.UP)
    articulation = abjad.Articulation("stopped")
    abjad.attach(articulation, target[1], direction=abjad.DOWN)
    articulation = abjad.Articulation("tenuto")
    abjad.attach(articulation, target[2])
    articulation = abjad.Articulation("staccatissimo")
    abjad.attach(articulation, target[3])
    articulation = abjad.Articulation("accent")
    abjad.attach(articulation, target[4])
    articulation = abjad.Articulation("staccato")
    abjad.attach(articulation, target[5])
    articulation = abjad.Articulation("portato")
    abjad.attach(articulation, target[6])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
            c''4
            ^ \marcato
            c''4
            _ \stopped
            c''4
            - \tenuto
            c''4
            - \staccatissimo
            c''4
            - \accent
            c''4
            - \staccato
            c''2
            - \portato
        }
        """
    )

    string = r"""\new Staff { c''4^^ c''_+ c''-- c''-! c''4-> c''-. c''2-_ }"""

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    for x in result:
        assert 1 == len(abjad.get.indicators(x, abjad.Articulation))


def test_LilyPondParser__indicators__Articulation_02():
    target = abjad.Staff([abjad.Note("c'", (1, 4))])
    articulation = abjad.Articulation("marcato")
    abjad.attach(articulation, target[0], direction=abjad.UP)
    articulation = abjad.Articulation("stopped")
    abjad.attach(articulation, target[0], direction=abjad.DOWN)
    articulation = abjad.Articulation("tenuto")
    abjad.attach(articulation, target[0])
    articulation = abjad.Articulation("staccatissimo")
    abjad.attach(articulation, target[0])
    articulation = abjad.Articulation("accent")
    abjad.attach(articulation, target[0])
    articulation = abjad.Articulation("staccato")
    abjad.attach(articulation, target[0])
    articulation = abjad.Articulation("portato")
    abjad.attach(articulation, target[0])

    string = r"""\new Staff { c'4 ^^ _+ -- -! -> -. -_ }"""

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    assert 7 == len(abjad.get.indicators(result[0], abjad.Articulation))


def test_LilyPondParser__indicators__Articulation_03():
    target = abjad.Container(
        abjad.makers.make_notes(
            ["c''", "c''", "b'", "c''"], [(1, 4), (1, 4), (1, 2), (1, 1)]
        )
    )

    articulation = abjad.Articulation("staccato")
    abjad.attach(articulation, target[0])
    articulation = abjad.Articulation("mordent")
    abjad.attach(articulation, target[1])
    articulation = abjad.Articulation("turn")
    abjad.attach(articulation, target[2])
    articulation = abjad.Articulation("fermata")
    abjad.attach(articulation, target[3])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            c''4
            - \staccato
            c''4
            - \mordent
            b'2
            - \turn
            c''1
            - \fermata
        }
        """
    )

    string = r"""{ c''4\staccato c''\mordent b'2\turn c''1\fermata }"""

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    for x in result:
        assert 1 == len(abjad.get.indicators(x, abjad.Articulation))


def test_LilyPondParser__indicators__BarLine_01():
    target = abjad.Staff(
        abjad.makers.make_notes(["e'", "d'", "c'"], [(1, 4), (1, 4), (1, 2)])
    )
    abjad.Score([target], name="Score")
    bar_line = abjad.BarLine("|.")
    abjad.attach(bar_line, target[-1])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
            e'4
            d'4
            c'2
            \bar "|."
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    items = abjad.get.indicators(result[2])
    assert 1 == len(items) and isinstance(items[0], abjad.BarLine)


def test_LilyPondParser__indicators__Beam_01():
    target = abjad.Voice(abjad.makers.make_notes([0] * 4, [(1, 8)]))
    abjad.beam(target[0:3])
    abjad.beam(target[3:], beam_lone_notes=True)

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            c'8
            c'8
            ]
            c'8
            [
            ]
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__indicators__Beam_02():
    target = abjad.Voice(abjad.makers.make_notes([0] * 4, [(1, 8)]))
    abjad.beam(target[:])
    abjad.beam(target[1:3])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            c'8
            [
            c'8
            ]
            c'8
            ]
        }
        """
    )

    with pytest.raises(Exception):
        abjad.LilyPondParser()(abjad.lilypond(target))


def test_LilyPondParser__indicators__Beam_03():
    target = abjad.Voice(abjad.makers.make_notes([0] * 4, [(1, 8)]))
    abjad.beam(target[:3])
    abjad.beam(target[2:])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            c'8
            c'8
            [
            ]
            c'8
            ]
        }
        """
    )

    with pytest.raises(Exception):
        abjad.LilyPondParser()(abjad.lilypond(target))


def test_LilyPondParser__indicators__Beam_04():
    string = "{ c'8 [ c'8 c'8 c'8 }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__Beam_05():
    """
    With direction.
    """

    target = abjad.Voice(abjad.makers.make_notes(4 * [0], [(1, 8)]))
    start_beam = abjad.StartBeam()
    abjad.attach(start_beam, target[0], direction=abjad.UP)
    stop_beam = abjad.StopBeam()
    abjad.attach(stop_beam, target[2])
    start_beam = abjad.StartBeam()
    abjad.attach(start_beam, target[3], direction=abjad.DOWN)
    stop_beam = abjad.StopBeam()
    abjad.attach(stop_beam, target[3])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            ^ [
            c'8
            c'8
            ]
            c'8
            _ [
            ]
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__indicators__Clef_01():
    target = abjad.Staff([abjad.Note(0, 1)])
    clef = abjad.Clef("bass")
    abjad.attach(clef, target[0])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \clef "bass"
            c'1
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    clefs = abjad.get.indicators(result[0], abjad.Clef)
    assert len(clefs) == 1


def test_LilyPondParser__indicators__Dynamic_01():
    target = abjad.Voice("c2 c2 c2 c2 c2 c2")
    dynamic = abjad.Dynamic("ppp")
    abjad.attach(dynamic, target[0], direction=abjad.DOWN)
    dynamic = abjad.Dynamic("mp")
    abjad.attach(dynamic, target[1], direction=abjad.UP)
    dynamic = abjad.Dynamic("rfz")
    abjad.attach(dynamic, target[2])
    dynamic = abjad.Dynamic("mf")
    abjad.attach(dynamic, target[3])
    dynamic = abjad.Dynamic("spp")
    abjad.attach(dynamic, target[4])
    dynamic = abjad.Dynamic("ff")
    abjad.attach(dynamic, target[5])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c2
            _ \ppp
            c2
            ^ \mp
            c2
            \rfz
            c2
            \mf
            c2
            \spp
            c2
            \ff
        }
        """
    )

    string = r"""\new Voice { c2 _ \ppp c ^ \mp c2\rfz c\mf c2\spp c\ff }"""
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result)
    for leaf in result:
        dynamics = abjad.get.indicators(leaf, abjad.Dynamic)
        assert len(dynamics) == 1


def test_LilyPondParser__indicators__Glissando_01():
    target = abjad.Container([abjad.Note(0, 1), abjad.Note(0, 1)])
    abjad.glissando(target[:])
    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__indicators__Glissando_02():
    string = r"{ c \glissando }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__Glissando_03():
    string = r"{ \glissando c }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__Hairpin_01():
    target = abjad.Voice(abjad.makers.make_notes([0] * 5, [(1, 4)]))
    abjad.hairpin("< !", target[:3])
    abjad.hairpin("> ppp", target[2:])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'4
            \<
            c'4
            c'4
            \!
            \>
            c'4
            c'4
            \ppp
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__indicators__Hairpin_02():
    """
    Dynamics can terminate hairpins.
    """

    target = abjad.Voice(abjad.makers.make_notes([0] * 3, [(1, 4)]))
    abjad.hairpin("<", target[0:2])
    abjad.hairpin("p > f", target[1:])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'4
            \<
            c'4
            \p
            \>
            c'4
            \f
        }
        """
    )

    string = r"\new Voice \relative c' { c \< c \p \> c \f }"
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__indicators__Hairpin_03():
    """
    Unterminated.
    """

    string = r"{ c \< c c c }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__Hairpin_04():
    """
    Unbegun is okay.
    """

    string = r"{ c c c c \! }"
    abjad.parser.LilyPondParser()(string)


def test_LilyPondParser__indicators__Hairpin_05():
    """
    No double dynamic spans permitted.
    """

    string = r"{ c \< \> c c c \! }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__Hairpin_06():
    """
    With direction.
    """

    target = abjad.Voice(abjad.makers.make_notes([0] * 5, [(1, 4)]))
    start_hairpin = abjad.StartHairpin("<")
    abjad.attach(start_hairpin, target[0], direction=abjad.UP)
    stop_hairpin = abjad.StopHairpin()
    abjad.attach(stop_hairpin, target[2])
    hairpin = abjad.StartHairpin(">")
    abjad.attach(hairpin, target[2], direction=abjad.DOWN)
    dynamic = abjad.Dynamic("ppp")
    abjad.attach(dynamic, target[-1])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'4
            ^ \<
            c'4
            c'4
            \!
            _ \>
            c'4
            c'4
            \ppp
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__indicators__Hairpin_07():
    string = r"\new Staff { c'4 ( \p \< d'4 e'4 f'4 ) \! }"
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(result) == abjad.string.normalize(
        r"""
        \new Staff
        {
            c'4
            \p
            (
            \<
            d'4
            e'4
            f'4
            )
            \!
        }
        """
    )


def test_LilyPondParser__indicators__HorizontalBracket_01():
    target = abjad.Voice(abjad.makers.make_notes([0] * 4, [(1, 4)]))
    abjad.horizontal_bracket(target[:])
    abjad.horizontal_bracket(target[:2])
    abjad.horizontal_bracket(target[2:])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'4
            \startGroup
            \startGroup
            c'4
            \stopGroup
            c'4
            \startGroup
            c'4
            \stopGroup
            \stopGroup
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__indicators__HorizontalBracket_02():
    """
    Starting and stopping on the same leaf.
    """

    string = r"""{ c \startGroup \stopGroup c c c }"""
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__HorizontalBracket_03():
    """
    One group stopping on a leaf, while another begins on the same leaf.
    """

    string = r"""{ c \startGroup c \stopGroup \startGroup c c \stopGroup }"""
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__HorizontalBracket_04():
    """
    Unterminated.
    """

    string = r"""{ c \startGroup c c c }"""
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__HorizontalBracket_05():
    """
    Unstarted.
    """

    string = r"""{ c c c c \stopGroup }"""
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__KeySignature_01():
    target = abjad.Staff([abjad.Note("fs'", 1)])
    key_signature = abjad.KeySignature(abjad.NamedPitchClass("g"), abjad.Mode("major"))
    abjad.attach(key_signature, target[0])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \key g \major
            fs'1
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    key_signatures = abjad.get.indicators(result[0], abjad.KeySignature)
    assert len(key_signatures) == 1


def test_LilyPondParser__indicators__Markup_01():
    target = abjad.Staff([abjad.Note(0, 1)])
    markup = abjad.Markup(r"\markup { hello! }")
    abjad.attach(markup, target[0], direction=abjad.UP)

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
            c'1
            ^ \markup { hello! }
        }
        """
    )

    string = r"""\new Staff { c'1 ^ "hello!" }"""

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    assert 1 == len(abjad.get.markup(result[0]))


def test_LilyPondParser__indicators__Markup_02():
    target = abjad.Staff([abjad.Note(0, (1, 4))])
    markup = abjad.Markup(r'\markup { X Y Z "a b c" }')
    abjad.attach(markup, target[0], direction=abjad.DOWN)

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
            c'4
            _ \markup { X Y Z "a b c" }
        }
        """
    ), repr(target)


def test_LilyPondParser__indicators__Markup_03():
    """
    Articulations following markup block are (re)lexed correctly after
    returning to the "notes" lexical state after popping the "markup lexical state.
    """

    target = abjad.Staff([abjad.Note(0, (1, 4)), abjad.Note(2, (1, 4))])
    markup = abjad.Markup(r"\markup { hello }")
    abjad.attach(markup, target[0], direction=abjad.UP)
    articulation = abjad.Articulation(".")
    abjad.attach(articulation, target[0])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
            c'4
            - \staccato
            ^ \markup { hello }
            d'4
        }
        """
    )

    string = r"""\new Staff { c' ^ \markup { hello } -. d' }"""

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    assert 1 == len(abjad.get.markup(result[0]))


def test_LilyPondParser__indicators__Markup_04():
    string_1 = r"""\markup { \bold { A B C } \italic 123 }"""

    string_2 = r"""\markup { \bold
    {
        A
        B
        C
    } \italic
    123 }"""

    parser = abjad.parser.LilyPondParser()
    markup = parser(string_1)
    assert abjad.lilypond(markup) == string_2


def test_LilyPondParser__indicators__MetronomeMark_01():
    target = abjad.Score([abjad.Staff([abjad.Note(0, 1)])])
    mark = abjad.MetronomeMark(textual_indication='"As fast as possible"')
    abjad.attach(mark, target[0][0], context="Staff")

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \tempo "As fast as possible"
                c'1
            }
        >>
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    leaves = abjad.select.leaves(result)
    leaf = leaves[0]
    marks = abjad.get.indicators(leaf, abjad.MetronomeMark)
    assert len(marks) == 1


def test_LilyPondParser__indicators__MetronomeMark_02():
    target = abjad.Score([abjad.Staff([abjad.Note(0, 1)])])
    leaves = abjad.select.leaves(target)
    mark = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
    abjad.attach(mark, leaves[0], context="Staff")

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \tempo 4=60
                c'1
            }
        >>
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    leaves = abjad.select.leaves(result)
    leaf = leaves[0]
    marks = abjad.get.indicators(leaf, abjad.MetronomeMark)
    assert len(marks) == 1


def test_LilyPondParser__indicators__MetronomeMark_03():
    target = abjad.Score([abjad.Staff([abjad.Note(0, 1)])])
    leaves = abjad.select.leaves(target)
    mark = abjad.MetronomeMark(abjad.Duration(1, 4), (59, 63))
    abjad.attach(mark, leaves[0], context="Staff")

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \tempo 4=59-63
                c'1
            }
        >>
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    leaves = abjad.select.leaves(result)
    leaf = leaves[0]
    marks = abjad.get.indicators(leaf, abjad.MetronomeMark)
    assert len(marks) == 1


def test_LilyPondParser__indicators__MetronomeMark_04():
    target = abjad.Score([abjad.Staff([abjad.Note(0, 1)])])
    mark = abjad.MetronomeMark(
        reference_duration=abjad.Duration(1, 4),
        units_per_minute=60,
        textual_indication='"Like a majestic swan, alive with youth and vigour!"',
    )
    leaves = abjad.select.leaves(target)
    abjad.attach(mark, leaves[0], context="Staff")

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \tempo "Like a majestic swan, alive with youth and vigour!" 4=60
                c'1
            }
        >>
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    leaves = abjad.select.leaves(result)
    leaf = leaves[0]
    marks = abjad.get.indicators(leaf, abjad.MetronomeMark)
    assert len(marks) == 1


def test_LilyPondParser__indicators__MetronomeMark_05():
    target = abjad.Score([abjad.Staff([abjad.Note(0, 1)])])
    mark = abjad.MetronomeMark(
        reference_duration=abjad.Duration(1, 16),
        units_per_minute=(34, 55),
        textual_indication='"Brighter than a thousand suns"',
    )
    leaves = abjad.select.leaves(target)
    abjad.attach(mark, leaves[0], context="Staff")

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \tempo "Brighter than a thousand suns" 16=34-55
                c'1
            }
        >>
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    leaves = abjad.select.leaves(result)
    leaf = leaves[0]
    marksn = abjad.get.indicators(leaf, abjad.MetronomeMark)
    assert len(marksn) == 1


def test_LilyPondParser__indicators__PhrasingSlur_01():
    """
    Successful slurs, showing single leaf overlap.
    """

    target = abjad.Voice(abjad.makers.make_notes([0] * 4, [(1, 4)]))
    abjad.phrasing_slur(target[2:])
    abjad.phrasing_slur(target[:3])
    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'4
            \(
            c'4
            c'4
            \)
            \(
            c'4
            \)
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__indicators__PhrasingSlur_02():
    """
    Swapped start and stop.
    """

    target = abjad.Voice(abjad.makers.make_notes([0] * 4, [(1, 4)]))
    abjad.phrasing_slur(target[2:])
    abjad.phrasing_slur(target[:3])
    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'4
            \(
            c'4
            c'4
            \)
            \(
            c'4
            \)
        }
        """
    )

    string = r"\new Voice \relative c' { c \( c c \( \) c \) }"
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__indicators__PhrasingSlur_03():
    """
    Single leaf.
    """

    string = r"{ c \( \) c c c }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__PhrasingSlur_04():
    """
    Unterminated.
    """

    string = r"{ c \( c c c }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__PhrasingSlur_05():
    """
    Unstarted.
    """

    string = r"{ c c c c \) }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__PhrasingSlur_06():
    """
    Nested.
    """

    string = r"{ c \( c \( c \) c \) }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__RepeatTie_01():
    target = abjad.Container([abjad.Note(0, 1), abjad.Note(0, 1)])
    repeat_tie = abjad.RepeatTie()
    abjad.attach(repeat_tie, target[-1])
    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__indicators__Slur_01():
    """
    Successful slurs, showing single leaf overlap.
    """

    target = abjad.Voice(abjad.makers.make_notes([0] * 4, [(1, 4)]))
    abjad.slur(target[2:])
    abjad.slur(target[:3])
    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'4
            (
            c'4
            c'4
            )
            (
            c'4
            )
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__indicators__Slur_02():
    """
    Swapped start and stop.
    """

    target = abjad.Voice(abjad.makers.make_notes([0] * 4, [(1, 4)]))
    abjad.slur(target[2:])
    abjad.slur(target[:3])
    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'4
            (
            c'4
            c'4
            )
            (
            c'4
            )
        }
        """
    )

    string = r"\new Voice \relative c' { c ( c c () c ) }"
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__indicators__Slur_03():
    """
    Single leaf.
    """

    string = "{ c () c c c }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__Slur_04():
    """
    Unterminated.
    """

    string = "{ c ( c c c }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__Slur_05():
    """
    Unstarted.
    """

    string = "{ c c c c ) }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__Slur_06():
    """
    Nested.
    """

    string = "{ c ( c ( c ) c ) }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__Slur_07():
    """
    With direction.
    """

    target = abjad.Voice(abjad.makers.make_notes([0] * 4, [(1, 4)]))
    start_slur = abjad.StartSlur()
    abjad.slur(target[:3], direction=abjad.DOWN, start_slur=start_slur)
    start_slur = abjad.StartSlur()
    abjad.slur(target[2:], direction=abjad.UP, start_slur=start_slur)
    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'4
            _ (
            c'4
            c'4
            )
            ^ (
            c'4
            )
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__indicators__StemTremolo_01():
    target = abjad.Staff([abjad.Note(0, 1)])
    stem_tremolo = abjad.StemTremolo(4)
    abjad.attach(stem_tremolo, target[0])
    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
            c'1
            :4
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    stem_tremolos = abjad.get.indicators(result[0], abjad.StemTremolo)
    assert 1 == len(stem_tremolos)


def test_LilyPondParser__indicators__Text_01():
    """
    Successful text spanners, showing single leaf overlap.
    """

    container = abjad.Voice(abjad.makers.make_notes([0] * 4, [(1, 4)]))
    abjad.text_spanner(container[2:])
    abjad.text_spanner(container[:3])
    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'4
            \startTextSpan
            c'4
            c'4
            \stopTextSpan
            \startTextSpan
            c'4
            \stopTextSpan
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(container))
    assert (
        abjad.lilypond(container) == abjad.lilypond(result) and container is not result
    )


def test_LilyPondParser__indicators__Text_02():
    """
    Swapped start and stop.
    """

    target = abjad.Voice(abjad.makers.make_notes([0] * 4, [(1, 4)]))
    abjad.text_spanner(target[2:])
    abjad.text_spanner(target[:3])
    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'4
            \startTextSpan
            c'4
            c'4
            \stopTextSpan
            \startTextSpan
            c'4
            \stopTextSpan
        }
        """
    )

    string = (
        r"\new Voice \relative c' { c \startTextSpan c c \startTextSpan \stopTextSpan c"
        r" \stopTextSpan }"
    )
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__indicators__Text_03():
    """
    Single leaf.
    """

    string = r"{ c \startTextSpan \stopTextSpan c c c }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__Text_04():
    """
    Unterminated.
    """

    string = r"{ c \startTextSpan c c c }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__Text_05():
    """
    Unstarted.
    """

    string = r"{ c c c c \stopTextSpan }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__Text_06():
    """
    Nested.
    """

    string = r"{ c \startTextSpan c \startTextSpan c \stopTextSpan c \stopTextSpan }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__Tie_01():
    target = abjad.Container([abjad.Note(0, 1), abjad.Note(0, 1)])
    abjad.tie(target[:])
    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__indicators__Tie_02():
    string = r"{ c ~ }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__Tie_03():
    string = r"{ ~ c }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__Tie_04():
    """
    With direction.
    """

    target = abjad.Container([abjad.Note(0, 1), abjad.Note(0, 1)])
    abjad.tie(target[:], direction=abjad.UP)
    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__indicators__Tie_05():
    """
    With direction.
    """

    target = abjad.Container([abjad.Note(0, 1), abjad.Note(0, 1)])
    abjad.tie(target[:], direction=abjad.DOWN)
    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__indicators__TimeSignature_01():
    target = abjad.Score([abjad.Staff([abjad.Note(0, 1)])])
    time_signature = abjad.TimeSignature((8, 8))
    abjad.attach(time_signature, target[0][0])
    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 8/8
                c'1
            }
        >>
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    leaves = abjad.select.leaves(result)
    leaf = leaves[0]
    time_signatures = abjad.get.indicators(leaf, abjad.TimeSignature)
    assert len(time_signatures) == 1


def test_LilyPondParser__indicators__Trill_01():
    """
    Successful trills, showing single leaf overlap.
    """

    notes = abjad.makers.make_notes(4 * [0], [(1, 4)])
    target = abjad.Voice(notes)
    abjad.trill_spanner(target[2:])
    abjad.trill_spanner(target[:3])
    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'4
            \startTrillSpan
            c'4
            c'4
            \stopTrillSpan
            \startTrillSpan
            c'4
            \stopTrillSpan
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__indicators__Trill_02():
    """
    Swapped start and stop.
    """

    notes = abjad.makers.make_notes(4 * [0], [(1, 4)])
    target = abjad.Voice(notes)
    abjad.trill_spanner(target[2:])
    abjad.trill_spanner(target[:3])
    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'4
            \startTrillSpan
            c'4
            c'4
            \stopTrillSpan
            \startTrillSpan
            c'4
            \stopTrillSpan
        }
        """
    )

    string = (
        r"\new Voice \relative c' { c \startTrillSpan c c \startTrillSpan \stopTrillSpan c"
        r" \stopTrillSpan }"
    )
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__indicators__Trill_03():
    """
    Single leaf.
    """

    string = r"{ c \startTrillSpan \stopTrillSpan c c c }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__Trill_04():
    """
    Unterminated.
    """

    string = r"{ c \startTrillSpan c c c }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__Trill_05():
    """
    Unstarted.
    """

    string = r"{ c c c c \stopTrillSpan }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__indicators__Trill_06():
    """
    Nested.
    """

    string = (
        r"{ c \startTrillSpan c \startTrillSpan c \stopTrillSpan c \stopTrillSpan }"
    )
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__leaves__Chord_01():
    target = abjad.Chord([0, 1, 4], (1, 4))
    parser = abjad.parser.LilyPondParser()
    result = parser("{ %s }" % abjad.lilypond(target))
    assert (
        abjad.lilypond(target) == abjad.lilypond(result[0]) and target is not result[0]
    )


def test_LilyPondParser__leaves__MultiMeasureRest_01():
    target = abjad.MultimeasureRest((1, 4))
    parser = abjad.parser.LilyPondParser()
    result = parser("{ %s }" % abjad.lilypond(target))
    assert (
        abjad.lilypond(target) == abjad.lilypond(result[0]) and target is not result[0]
    )


def test_LilyPondParser__leaves__Note_01():
    target = abjad.Note(0, 1)
    parser = abjad.parser.LilyPondParser()
    result = parser("{ %s }" % abjad.lilypond(target))
    assert (
        abjad.lilypond(target) == abjad.lilypond(result[0]) and target is not result[0]
    )


def test_LilyPondParser__leaves__Rest_01():
    target = abjad.Rest((1, 8))
    parser = abjad.parser.LilyPondParser()
    result = parser("{ %s }" % abjad.lilypond(target))
    assert (
        abjad.lilypond(target) == abjad.lilypond(result[0]) and target is not result[0]
    )


def test_LilyPondParser__leaves__Skip_01():
    target = abjad.Skip((3, 8))
    parser = abjad.parser.LilyPondParser()
    result = parser("{ %s }" % abjad.lilypond(target))
    assert (
        abjad.lilypond(target) == abjad.lilypond(result[0]) and target is not result[0]
    )


def test_LilyPondParser__lilypondfile__LilyPondFile_01():
    string = "{ c } { c } { c } { c }"
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert isinstance(result, abjad.LilyPondFile)


def test_LilyPondParser__lilypondfile__ScoreBlock_01():
    target = abjad.Block(name="score")
    target.items.append(abjad.Score())
    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__misc__chord_repetition_01():
    target = abjad.Container(
        [
            abjad.Chord([0, 4, 7], (1, 4)),
            abjad.Chord([0, 4, 7], (1, 4)),
            abjad.Chord([0, 4, 7], (1, 4)),
            abjad.Chord([0, 4, 7], (1, 4)),
        ]
    )

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            <c' e' g'>4
            <c' e' g'>4
            <c' e' g'>4
            <c' e' g'>4
        }
        """
    )

    string = r"""{ <c' e' g'> q q q }"""
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__misc__chord_repetition_02():
    target = abjad.Voice(
        [
            abjad.Chord([0, 4, 7], (1, 8)),
            abjad.Chord([0, 4, 7], (1, 8)),
            abjad.Chord([0, 4, 7], (1, 4)),
            abjad.Chord([0, 4, 7], (3, 16)),
            abjad.Chord([0, 4, 7], (1, 16)),
            abjad.Chord([0, 4, 7], (1, 4)),
        ]
    )
    dynamic = abjad.Dynamic("p")
    abjad.attach(dynamic, target[0])
    articulation = abjad.Articulation("staccatissimo")
    abjad.attach(articulation, target[2])
    markup = abjad.Markup(r"\markup { text }")
    abjad.attach(markup, target[3], direction=abjad.UP)
    articulation = abjad.Articulation("staccatissimo")
    abjad.attach(articulation, target[-1])
    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Voice
        {
            <c' e' g'>8
            \p
            <c' e' g'>8
            <c' e' g'>4
            - \staccatissimo
            <c' e' g'>8.
            ^ \markup { text }
            <c' e' g'>16
            <c' e' g'>4
            - \staccatissimo
        }
        """
    )

    string = r"""\new Voice { <c' e' g'>8\p q q4-! q8.^"text" q16 q4-! }"""
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__misc__chord_repetition_03():
    target = abjad.Container(
        [
            abjad.Chord([0, 4, 7], (1, 8)),
            abjad.Note(12, (1, 8)),
            abjad.Chord([0, 4, 7], (1, 8)),
            abjad.Note(12, (1, 8)),
            abjad.Rest((1, 4)),
            abjad.Chord([0, 4, 7], (1, 4)),
        ]
    )

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            <c' e' g'>8
            c''8
            <c' e' g'>8
            c''8
            r4
            <c' e' g'>4
        }
        """
    )

    string = r"""{ <c' e' g'>8 c'' q c'' r4 q }"""
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__misc__comments_01():
    """
    Comments are ignored.
    """

    target = abjad.Staff()
    string = r"""\new Staff { %{ HOO HAH %} }"""
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__misc__default_duration_01():
    target = abjad.Container(
        abjad.makers.make_notes(
            [0], [(1, 4), (1, 2), (1, 2), (1, 8), (1, 8), (3, 16), (3, 16)]
        )
    )
    target[-2].multiplier = (5, 17)
    target[-1].multiplier = (5, 17)
    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            c'4
            c'2
            c'2
            c'8
            c'8
            c'8. * 5/17
            c'8. * 5/17
        }
        """
    )

    string = r"""{ c' c'2 c' c'8 c' c'8. * 5/17 c' }"""
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__misc__variables_01():
    target = abjad.Staff(
        [
            abjad.Container(
                [
                    abjad.Container(
                        [
                            abjad.Container(
                                [
                                    abjad.Container([abjad.Note(0, (1, 8))]),
                                    abjad.Note(2, (1, 8)),
                                    abjad.Note(4, (1, 4)),
                                ]
                            ),
                            abjad.Note(5, (1, 4)),
                            abjad.Note(7, (1, 2)),
                        ]
                    ),
                    abjad.Note(9, (1, 2)),
                    abjad.Note(11, 1),
                ]
            ),
            abjad.Note(12, 1),
        ]
    )

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
            {
                {
                    {
                        {
                            c'8
                        }
                        d'8
                        e'4
                    }
                    f'4
                    g'2
                }
                a'2
                b'1
            }
            c''1
        }
        """
    )

    string = r"""
        foo = { c'8 }
        foo = { \foo d' e'4 }
        foo = { \foo f' g'2 }
        foo = { \foo a' b'1 }
        \new Staff { \foo c'' }
    """

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__misc__version_string_01():
    """
    Version strings are ignored.
    """

    target = abjad.Staff()
    string = r"""\version "2.14.2" \new Staff { }"""
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser_accidentals_cautionary_01():
    string = "{ c?4 }"
    parsed = abjad.parser.LilyPondParser()(string)
    assert parsed[0].note_head.is_cautionary is True
    assert abjad.lilypond(parsed[0]) == "c?4"


def test_LilyPondParser_accidentals_cautionary_02():
    string = "{ <c? e g??>4 }"
    parsed = abjad.parser.LilyPondParser()(string)
    assert parsed[0].note_heads[0].is_cautionary is True
    assert parsed[0].note_heads[1].is_cautionary is False
    assert parsed[0].note_heads[2].is_cautionary is True
    assert abjad.lilypond(parsed[0]) == "<c? e g?>4"


def test_LilyPondParser_accidentals_forced_01():
    string = "{ c!4 }"
    parsed = abjad.parser.LilyPondParser()(string)
    assert parsed[0].note_head.is_forced is True
    assert abjad.lilypond(parsed[0]) == "c!4"


def test_LilyPondParser_accidentals_forced_02():
    string = "{ <c! e g!!>4 }"
    parsed = abjad.parser.LilyPondParser()(string)
    assert parsed[0].note_heads[0].is_forced is True
    assert parsed[0].note_heads[1].is_forced is False
    assert parsed[0].note_heads[2].is_forced is True
    assert abjad.lilypond(parsed[0]) == "<c! e g!>4"


def test_rhythmtrees_parse_01():
    string = "(3 (1 (3 (1 (3 (1 (3 (1 1 1 1))))))))"
    nodes = abjad.rhythmtrees.parse(string)
    components = abjad.rhythmtrees.call(nodes)
    voice = abjad.Voice(components)
    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            \tweak text #tuplet-number::calc-fraction-text
            \tuplet 4/3
            {
                c'4
                \tweak text #tuplet-number::calc-fraction-text
                \tuplet 4/3
                {
                    c'4
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 4/3
                    {
                        c'4
                        \tweak text #tuplet-number::calc-fraction-text
                        \tuplet 4/3
                        {
                            c'4
                            c'4
                            c'4
                            c'4
                        }
                    }
                }
            }
        }
        """
    )
