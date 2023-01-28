import abjad


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
