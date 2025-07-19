import abjad


def test_wrapper_Wrapper___copy___01():
    """
    Wrapper copy preserves annotation.
    """

    staff_1 = abjad.Staff("c'4 d'4 e'4 f'4")
    abjad.annotate(staff_1[0], "color", "red")

    assert abjad.get.annotation(staff_1[0], "color") == "red"

    staff_2 = abjad.mutate.copy(staff_1)

    assert abjad.get.annotation(staff_2[0], "color") == "red"


def test_wrapper_Wrapper___copy___02():
    """
    Wrapper copy preserves tag.
    """

    staff_1 = abjad.Staff("c'4 d'4 e'4 f'4")
    clef = abjad.Clef("alto")
    tag = abjad.Tag("RED")
    abjad.attach(clef, staff_1[0], tag=tag)
    wrapper = abjad.get.wrapper(staff_1[0], abjad.Clef)

    assert wrapper.get_tag() == tag

    staff_2 = abjad.mutate.copy(staff_1)
    wrapper = abjad.get.wrapper(staff_2[0], abjad.Clef)

    assert wrapper.get_tag() == tag


def test_wrapper_Wrapper___copy___03():
    """
    Wrapper copy preserves deactivate flag.
    """

    staff_1 = abjad.Staff("c'4 d'4 e'4 f'4")
    clef = abjad.Clef("alto")
    abjad.attach(clef, staff_1[0], deactivate=True, tag=abjad.Tag("RED"))
    wrapper_1 = abjad.get.wrapper(staff_1[0], abjad.Clef)

    assert wrapper_1.get_deactivate() is True

    staff_2 = abjad.mutate.copy(staff_1)
    wrapper_2 = abjad.get.wrapper(staff_2[0], abjad.Clef)

    assert wrapper_2.get_deactivate() is True
