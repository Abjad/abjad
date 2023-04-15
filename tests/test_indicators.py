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
    with pytest.raises(Exception):
        abjad.attach(abjad.Clef("treble"), staff[0])


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
