import abjad


def test_mutate__set_leaf_duration_01():
    """
    Change leaf to tied duration.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:2])

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
            e'8
            f'8
        }
        """
    ), print(abjad.lilypond(voice))

    abjad.mutate._set_leaf_duration(voice[1], abjad.Duration(5, 32))

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
            ~
            d'32
            ]
            e'8
            f'8
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate__set_leaf_duration_02():
    """
    Change tied leaf to tied value.
    Duplicate ties are not created.
    """

    voice = abjad.Voice("c'8 c'8 c'8 c'8")
    abjad.tie(voice[:2])
    abjad.beam(voice[:2])

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            ~
            [
            c'8
            ]
            c'8
            c'8
        }
        """
    ), print(abjad.lilypond(voice))

    abjad.mutate._set_leaf_duration(voice[1], abjad.Duration(5, 32))

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            ~
            c'8
            ]
            ~
            c'32
            ]
            c'8
            c'8
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate__set_leaf_duration_03():
    """
    Change leaf to nontied duration.
    Same as voice.written_duration = abjad.Duration(3, 16).
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:2])

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
            e'8
            f'8
        }
        """
    ), print(abjad.lilypond(voice))

    abjad.mutate._set_leaf_duration(voice[1], abjad.Duration(3, 16))

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8.
            ]
            e'8
            f'8
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate__set_leaf_duration_04():
    """
    Change leaf to tied duration without power-of-two denominator.
    abjad.Tuplet inserted over new tied notes.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:2])

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
            e'8
            f'8
        }
        """
    ), print(abjad.lilypond(voice))

    abjad.mutate._set_leaf_duration(voice[1], abjad.Duration(5, 48))

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                d'8
                ]
                ~
                d'32
                ]
            }
            e'8
            f'8
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate__set_leaf_duration_05():
    """
    Change leaf to untied duration without power-of-two denominator.
    Tuplet inserted over input leaf.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.beam(voice[:2])

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            ]
            e'8
            f'8
        }
        """
    ), print(abjad.lilypond(voice))

    abjad.mutate._set_leaf_duration(voice[1], abjad.Duration(1, 12))

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                d'8
                ]
            }
            e'8
            f'8
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)


def test_mutate__set_leaf_duration_06():
    """
    Change leaf with LilyPond multiplier to untied duration with
    power-of-two denominator. LilyPond multiplier changes but leaf written
    duration does not.
    """

    note = abjad.Note(0, (1, 8), multiplier=(1, 2))

    assert abjad.lilypond(note) == "c'8 * 1/2"

    abjad.mutate._set_leaf_duration(note, abjad.Duration(1, 32))

    assert abjad.wf.wellformed(note)
    assert abjad.lilypond(note) == "c'8 * 1/4"


def test_mutate__set_leaf_duration_07():
    """
    Change leaf with LilyPond multiplier to untied duration with
    power-of-two denominator. LilyPond multiplier changes but leaf
    written duration does not.
    """

    note = abjad.Note(0, (1, 8), multiplier=(1, 2))

    assert abjad.lilypond(note) == "c'8 * 1/2"

    abjad.mutate._set_leaf_duration(note, abjad.Duration(3, 32))

    assert abjad.wf.wellformed(note)
    assert abjad.lilypond(note) == "c'8 * 3/4"


def test_mutate__set_leaf_duration_08():
    """
    Change leaf with LilyPond multiplier to tied duration with
    power-of-two denominator. LilyPond multiplier changes but leaf
    written duration does not.
    """

    note = abjad.Note(0, (1, 8), multiplier=(1, 2))

    assert abjad.lilypond(note) == "c'8 * 1/2"

    abjad.mutate._set_leaf_duration(note, abjad.Duration(5, 32))

    assert abjad.wf.wellformed(note)
    assert abjad.lilypond(note) == "c'8 * 5/4"


def test_mutate__set_leaf_duration_09():
    """
    Change leaf with LilyPond multiplier to duration without
    power-of-two denominator. LilyPond multiplier changes but leaf
    written duration does not.
    """

    note = abjad.Note(0, (1, 8), multiplier=(1, 2))

    assert abjad.lilypond(note) == "c'8 * 1/2"

    abjad.mutate._set_leaf_duration(note, abjad.Duration(1, 24))

    assert abjad.wf.wellformed(note)
    assert abjad.lilypond(note) == "c'8 * 1/3"


def test_mutate__set_leaf_duration_10():
    """
    Change leaf with LilyPond multiplier.
    Change to tie-necessitating duration without power-of-two denominator.
    LilyPond multiplier changes but leaf written duration does not.
    """

    note = abjad.Note(0, (1, 8), multiplier=(1, 2))

    assert abjad.lilypond(note) == "c'8 * 1/2"

    abjad.mutate._set_leaf_duration(note, abjad.Duration(5, 24))

    assert abjad.wf.wellformed(note)
    assert abjad.lilypond(note) == "c'8 * 5/3"


def test_mutate__set_leaf_duration_11():
    """
    Change rest duration.
    """

    voice = abjad.Voice("c'8 r8 e'8 f'8")
    abjad.beam(voice[:3])

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            r8
            e'8
            ]
            f'8
        }
        """
    ), print(abjad.lilypond(voice))

    abjad.mutate._set_leaf_duration(voice[1], abjad.Duration(5, 32))

    assert abjad.lilypond(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            r8
            r32
            e'8
            ]
            f'8
        }
        """
    ), print(abjad.lilypond(voice))

    assert abjad.wf.wellformed(voice)
