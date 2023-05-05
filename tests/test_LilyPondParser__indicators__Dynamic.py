import abjad


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
