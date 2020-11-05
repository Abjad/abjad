import abjad


def test_get_has_indicator_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.attach("foo", staff[0])

    assert not abjad.get.has_indicator(staff, str)
    assert abjad.get.has_indicator(staff[0], str)
    assert not abjad.get.has_indicator(staff[1], str)
    assert not abjad.get.has_indicator(staff[2], str)
    assert not abjad.get.has_indicator(staff[3], str)


def test_get_has_indicator_02():

    staff = abjad.Staff("c'2 d'2")
    articulation = abjad.Articulation("staccato")
    abjad.attach(articulation, staff[0])

    assert abjad.get.has_indicator(staff[0], abjad.Articulation)
    assert not abjad.get.has_indicator(staff[1], abjad.Duration)


def test_get_has_indicator_03():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    command = abjad.LilyPondLiteral(r"\break", "closing")
    abjad.attach(command, staff[-1])

    assert not abjad.get.has_indicator(staff[0], abjad.LilyPondLiteral)
    assert not abjad.get.has_indicator(staff[1], abjad.LilyPondLiteral)
    assert not abjad.get.has_indicator(staff[2], abjad.LilyPondLiteral)
    assert abjad.get.has_indicator(staff[3], abjad.LilyPondLiteral)


def test_get_has_indicator_04():

    staff = abjad.Staff("c'2 d'2")
    comment = abjad.LilyPondComment("comment")
    abjad.attach(comment, staff[0])

    assert abjad.get.has_indicator(staff[0], abjad.LilyPondComment)
    assert not abjad.get.has_indicator(staff[1], abjad.LilyPondComment)


def test_get_has_indicator_05():

    staff = abjad.Staff("c'2 d'2")
    stem_tremolo = abjad.StemTremolo(16)
    abjad.attach(stem_tremolo, staff[0])

    assert abjad.get.has_indicator(staff[0], abjad.StemTremolo)
    assert not abjad.get.has_indicator(staff[1], abjad.StemTremolo)


def test_get_has_indicator_06():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    time_signature = abjad.TimeSignature((4, 8))
    abjad.attach(time_signature, staff[0])

    assert abjad.get.has_indicator(staff[0], abjad.TimeSignature)
    assert not abjad.get.has_indicator(staff[1])
    assert not abjad.get.has_indicator(staff[2])
    assert not abjad.get.has_indicator(staff[3])
    assert not abjad.get.has_indicator(staff)
