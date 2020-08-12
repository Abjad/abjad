import abjad


def test_LilyPondParser__indicators__Markup_01():

    target = abjad.Staff([abjad.Note(0, 1)])
    markup = abjad.Markup("hello!", direction=abjad.Up)
    abjad.attach(markup, target[0])

    assert abjad.lilypond(target) == abjad.String.normalize(
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
    markup = abjad.Markup(["X", "Y", "Z", "a b c"], direction=abjad.Down)
    abjad.attach(markup, target[0])

    assert abjad.lilypond(target) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            _ \markup {
                X
                Y
                Z
                "a b c"
                }
        }
        """
    )

    string = r"""\new Staff { c' _ \markup { X Y Z "a b c" } }"""

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    assert 1 == len(abjad.get.markup(result[0]))


def test_LilyPondParser__indicators__Markup_03():
    """
    Articulations following markup block are (re)lexed correctly after
    returning to the "notes" lexical state after popping the "markup lexical state.
    """

    target = abjad.Staff([abjad.Note(0, (1, 4)), abjad.Note(2, (1, 4))])
    markup = abjad.Markup("hello", direction=abjad.Up)
    abjad.attach(markup, target[0])
    articulation = abjad.Articulation(".")
    abjad.attach(articulation, target[0])

    assert abjad.lilypond(target) == abjad.String.normalize(
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

    command1 = abjad.MarkupCommand("bold", ["A", "B", "C"])
    command2 = abjad.MarkupCommand("italic", "123")
    markup = abjad.Markup((command1, command2))

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(markup))

    assert isinstance(result, abjad.Markup)
    assert abjad.lilypond(result) == abjad.lilypond(markup)
