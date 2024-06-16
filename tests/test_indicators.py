import pytest

import abjad


def test_indicators_01():
    """
    Classes ignore "hide" in definitions of __eq__.

    Test will be removed when "hide" migrates from indicators to wrapper.
    """

    assert abjad.Clef("treble", hide=False) == abjad.Clef("treble", hide=False)
    assert abjad.Clef("treble", hide=False) == abjad.Clef("treble", hide=True)
    assert abjad.Clef("treble", hide=True) == abjad.Clef("treble", hide=False)
    assert abjad.Clef("treble", hide=True) == abjad.Clef("treble", hide=True)
    assert abjad.Clef("treble", hide=False) != abjad.Clef("alto", hide=False)
    assert abjad.Clef("treble", hide=False) != abjad.Clef("alto", hide=True)
    assert abjad.Clef("treble", hide=True) != abjad.Clef("alto", hide=False)
    assert abjad.Clef("treble", hide=True) != abjad.Clef("alto", hide=True)

    assert abjad.Dynamic("p", hide=False) == abjad.Dynamic("p", hide=False)
    assert abjad.Dynamic("p", hide=False) == abjad.Dynamic("p", hide=True)
    assert abjad.Dynamic("p", hide=True) == abjad.Dynamic("p", hide=False)
    assert abjad.Dynamic("p", hide=True) == abjad.Dynamic("p", hide=True)
    assert abjad.Dynamic("p", hide=False) != abjad.Dynamic("f", hide=False)
    assert abjad.Dynamic("p", hide=False) != abjad.Dynamic("f", hide=True)
    assert abjad.Dynamic("p", hide=True) != abjad.Dynamic("f", hide=False)
    assert abjad.Dynamic("p", hide=True) != abjad.Dynamic("f", hide=True)

    assert abjad.MetronomeMark(
        abjad.Duration(1, 4), 60, hide=False
    ) == abjad.MetronomeMark(abjad.Duration(1, 4), 60, hide=False)
    assert abjad.MetronomeMark(
        abjad.Duration(1, 4), 60, hide=False
    ) == abjad.MetronomeMark(abjad.Duration(1, 4), 60, hide=True)
    assert abjad.MetronomeMark(
        abjad.Duration(1, 4), 60, hide=True
    ) == abjad.MetronomeMark(abjad.Duration(1, 4), 60, hide=False)
    assert abjad.MetronomeMark(
        abjad.Duration(1, 4), 60, hide=True
    ) == abjad.MetronomeMark(abjad.Duration(1, 4), 60, hide=True)
    assert abjad.MetronomeMark(
        abjad.Duration(1, 4), 60, hide=False
    ) != abjad.MetronomeMark(abjad.Duration(1, 4), 72, hide=False)
    assert abjad.MetronomeMark(
        abjad.Duration(1, 4), 60, hide=False
    ) != abjad.MetronomeMark(abjad.Duration(1, 4), 72, hide=True)
    assert abjad.MetronomeMark(
        abjad.Duration(1, 4), 60, hide=True
    ) != abjad.MetronomeMark(abjad.Duration(1, 4), 72, hide=False)
    assert abjad.MetronomeMark(
        abjad.Duration(1, 4), 60, hide=True
    ) != abjad.MetronomeMark(abjad.Duration(1, 4), 72, hide=True)

    assert abjad.TimeSignature(((3, 4)), hide=False) == abjad.TimeSignature(
        ((3, 4)), hide=False
    )
    assert abjad.TimeSignature(((3, 4)), hide=False) == abjad.TimeSignature(
        ((3, 4)), hide=True
    )
    assert abjad.TimeSignature(((3, 4)), hide=True) == abjad.TimeSignature(
        ((3, 4)), hide=False
    )
    assert abjad.TimeSignature(((3, 4)), hide=True) == abjad.TimeSignature(
        ((3, 4)), hide=True
    )
    assert abjad.TimeSignature(((3, 4)), hide=False) != abjad.TimeSignature(
        ((4, 4)), hide=False
    )
    assert abjad.TimeSignature(((3, 4)), hide=False) != abjad.TimeSignature(
        ((4, 4)), hide=True
    )
    assert abjad.TimeSignature(((3, 4)), hide=True) != abjad.TimeSignature(
        ((4, 4)), hide=False
    )
    assert abjad.TimeSignature(((3, 4)), hide=True) != abjad.TimeSignature(
        ((4, 4)), hide=True
    )


# TODO: parameterize each test below:


def test_indicators_02():
    """
    Conditions:
        * indicator_1, indicator_2 attach to same leaf
        * class(indicator_1) is class(indicator_2)
        * indicator_1 == indicator_2
        * indicator_1.hide == indicator_2.hide == False
    Result:
        * raises exception
    """
    staff = abjad.Staff("c'4 d' e' f'")
    abjad.attach(abjad.Clef("treble"), staff[0])
    with pytest.raises(Exception) as e:
        abjad.attach(abjad.Clef("treble"), staff[0])
    assert "attempting to attach conflicting indicator" in str(e)
    """
    abjad.attach(abjad.VoiceNumber(1), staff[0])
    with pytest.raises(Exception) as e:
        abjad.attach(abjad.VoiceNumber(1), staff[0])
    assert "attempting to attach conflicting indicator" in str(e)
    """


def test_indicators_03():
    """
    Conditions:
        * indicator_1, indicator_2 attach to same leaf
        * class(indicator_1) is class(indicator_2)
        * indicator_1 != indicator_2
        * indicator_1.hide == indicator_2.hide == False
    Result:
        * raises exception
    """
    staff = abjad.Staff("c'4 d' e' f'")
    abjad.attach(abjad.Clef("treble"), staff[0])
    with pytest.raises(Exception):
        abjad.attach(abjad.Clef("alto"), staff[0])


def test_indicators_04():
    """
    Conditions:
        * indicator_1, indicator_2 attach to same leaf
        * class(indicator_1) is class(indicator_2)
        * indicator_1 == indicator_2
        * indicator_1.hide == indicator_2.hide == True
    Result:
        * raises exception
    """
    staff = abjad.Staff("c'4 d' e' f'")
    abjad.attach(abjad.Clef("treble", hide=True), staff[0])
    with pytest.raises(Exception):
        abjad.attach(abjad.Clef("treble", hide=True), staff[0])


def test_indicators_05():
    """
    Conditions:
        * indicator_1, indicator_2 attach to same leaf
        * class(indicator_1) is class(indicator_2)
        * indicator_1 == indicator_2
        * indicator_1.hide == False and indicator_2.hide == True
    Result:
        * raises exception
    """
    staff = abjad.Staff("c'4 d' e' f'")
    abjad.attach(abjad.Clef("treble"), staff[0])
    with pytest.raises(Exception):
        abjad.attach(abjad.Clef("treble", hide=True), staff[0])


def test_indicators_06():
    """
    Conditions:
        * indicator_1, indicator_2 attach to same leaf
        * class(indicator_1) is class(indicator_2)
        * indicator_1 == indicator_2
        * indicator_1.hide == True and indicator_2.hide == False
    Result:
        * raises exception
    """
    staff = abjad.Staff("c'4 d' e' f'")
    abjad.attach(abjad.Clef("treble", hide=True), staff[0])
    with pytest.raises(Exception):
        abjad.attach(abjad.Clef("treble"), staff[0])


def test_indicators_07():
    """
    Conditions:
        * indicator_1, indicator_2 attach to same leaf
        * class(indicator_1) is class(indicator_2)
        * indicator_1 =! indicator_2
        * indicator_1.hide == False and indicator_2.hide == True
    Result:
        * ok
    """
    staff = abjad.Staff("c'4 d' e' f'")
    abjad.attach(abjad.Clef("treble"), staff[0])
    abjad.attach(abjad.Clef("alto", hide=True), staff[0])


def test_indicators_08():
    """
    Conditions:
        * indicator_1, indicator_2 attach to same leaf
        * class(indicator_1) is class(indicator_2)
        * indicator_1 != indicator_2
        * indicator_1.hide == True and indicator_2.hide == False
    Result:
        * ok
    """
    staff = abjad.Staff("c'4 d' e' f'")
    abjad.attach(abjad.Clef("treble", hide=True), staff[0])
    abjad.attach(abjad.Clef("alto"), staff[0])


def test_indicators_09():
    """
    Conditions:
        * indicator_1, indicator_2 attach to same leaf
        * class(indicator_1) is class(indicator_2)
        * indicator_1 == indicator_2
        * indicator_1.site != indicator_2.site
    Result:
        * ok
    """
    voice = abjad.Voice("c'4", name="Voice")
    staff = abjad.Staff([voice], name="Staff")
    abjad.Score([staff], name="Score")
    abjad.attach(abjad.BarLine("|", site="before"), voice[0])
    abjad.attach(abjad.BarLine("|", site="after"), voice[0])

    # TODO: this should raise some other type of exception
    #       having to do with redundancy because ottava 1
    #       followed later by ottava 1 is redundant;
    #       this arises only for persistent indicators
    voice = abjad.Voice("c'4", name="Voice")
    staff = abjad.Staff([voice], name="Staff")
    abjad.Score([staff], name="Score")
    abjad.attach(abjad.Ottava(1, site="before"), voice[0])
    abjad.attach(abjad.Ottava(1, site="after"), voice[0])


def test_indicators_10():
    """
    Conditions:
        * indicator_1, indicator_2 attach to same leaf
        * class(indicator_1) is class(indicator_2)
        * indicator_1 != indicator_2
        * indicator_1.site != indicator_2.site
    Result:
        * ok
    """
    voice = abjad.Voice("c'4", name="Voice")
    staff = abjad.Staff([voice], name="Staff")
    abjad.Score([staff], name="Score")
    abjad.attach(abjad.BarLine("|", site="before"), voice[0])
    abjad.attach(abjad.BarLine("||", site="after"), voice[0])

    voice = abjad.Voice("c'4", name="Voice")
    staff = abjad.Staff([voice], name="Staff")
    abjad.Score([staff], name="Score")
    abjad.attach(abjad.Ottava(1, site="before"), voice[0])
    abjad.attach(abjad.Ottava(0, site="after"), voice[0])


def test_indicators_11():
    """
    Conditions:
        * indicator_1, indicator_2 attach to same leaf
        * class(indicator_1) is class(indicator_2)
        * indicator_1 == indicator_2
        * indicator_1.site == indicator_2.site
    Result:
        * exception
    """
    voice = abjad.Voice("c'4", name="Voice")
    staff = abjad.Staff([voice], name="Staff")
    abjad.Score([staff], name="Score")
    abjad.attach(abjad.BarLine("|", site="after"), voice[0])
    with pytest.raises(Exception) as e:
        abjad.attach(abjad.BarLine("|", site="after"), voice[0])
    assert "attempting to attach conflicting indicator" in str(e)

    voice = abjad.Voice("c'4", name="Voice")
    staff = abjad.Staff([voice], name="Staff")
    abjad.Score([staff], name="Score")
    abjad.attach(abjad.Ottava(1, site="before"), voice[0])
    with pytest.raises(Exception) as e:
        abjad.attach(abjad.Ottava(1, site="before"), voice[0])
    assert "attempting to attach conflicting indicator" in str(e)


def test_indicators_12():
    """
    Conditions:
        * indicator_1, indicator_2 attach to same leaf
        * class(indicator_1) is class(indicator_2)
        * indicator_1 != indicator_2
        * indicator_1.site == indicator_2.site
    Result:
        * exception
    """
    voice = abjad.Voice("c'4", name="Voice")
    staff = abjad.Staff([voice], name="Staff")
    abjad.Score([staff], name="Score")
    abjad.attach(abjad.BarLine("|", site="after"), voice[0])
    with pytest.raises(Exception) as e:
        abjad.attach(abjad.BarLine("||", site="after"), voice[0])
    assert "attempting to attach conflicting indicator" in str(e)

    voice = abjad.Voice("c'4", name="Voice")
    staff = abjad.Staff([voice], name="Staff")
    abjad.Score([staff], name="Score")
    abjad.attach(abjad.Ottava(1, site="before"), voice[0])
    with pytest.raises(Exception) as e:
        abjad.attach(abjad.Ottava(0, site="before"), voice[0])
    assert "attempting to attach conflicting indicator" in str(e)


def test_allowable_sites():
    """
    Indicators with "allowable_sites" property behave like this.
    """

    voice = abjad.Voice("c'4")
    literal = abjad.LilyPondLiteral("% leaf comment", site="before")
    abjad.attach(literal, voice[0])
    literal = abjad.LilyPondLiteral("% container comment", site="opening")
    abjad.attach(literal, voice)
    literal = abjad.LilyPondLiteral("% container comment", site="opening")
    with pytest.raises(Exception) as e:
        abjad.attach(literal, voice[0])
    assert "allows only" in str(e)


def test_StartTrillSpan_01():
    """
    Set force_trill_pitch_head_accidental=True to force trill pitch head accidental.
    """

    voice = abjad.Voice("c'4 d' e' f'")
    start_trill_span = abjad.StartTrillSpan(
        pitch=abjad.NamedPitch("D4"),
        force_trill_pitch_head_accidental=True,
    )
    abjad.attach(start_trill_span, voice[0])
    stop_trill_span = abjad.StopTrillSpan()
    abjad.attach(stop_trill_span, voice[-1])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            \pitchedTrill
            c'4
            \startTrillSpan d'!
            d'4
            e'4
            f'4
            \stopTrillSpan
        }
        """
    )
