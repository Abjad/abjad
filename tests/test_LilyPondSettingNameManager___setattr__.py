import abjad


def test_LilyPondSettingNameManager___setattr___01():
    """
    Define LilyPond autoBeaming context abjad.setting.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.setting(staff).auto_beaming = True

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            autoBeaming = ##t
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
    )

    assert abjad.inspect(staff).wellformed()


def test_LilyPondSettingNameManager___setattr___02():
    """
    Remove LilyPond autoBeaming context abjad.setting.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.setting(staff).auto_beaming = True
    del abjad.setting(staff).auto_beaming

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
    )

    assert abjad.inspect(staff).wellformed()


def test_LilyPondSettingNameManager___setattr___03():
    """
    Define LilyPond currentBarNumber context abjad.setting.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.setting(staff[0]).score.current_bar_number = 12

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \set Score.currentBarNumber = #12
            c'8
            d'8
            e'8
            f'8
        }
        """
    )

    assert abjad.inspect(staff).wellformed()


def test_LilyPondSettingNameManager___setattr___04():
    """
    Define LilyPond currentBarNumber context abjad.setting.
    """

    staff = abjad.Staff()
    staff.append(abjad.Container("c'8 d'8"))
    staff.append(abjad.Container("e'8 f'8"))
    abjad.setting(staff[0]).score.current_bar_number = 12

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \set Score.currentBarNumber = #12
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
        }
        """
    )

    assert abjad.inspect(staff).wellformed()


def test_LilyPondSettingNameManager___setattr___05():
    """
    Define LilyPond fontSize context abjad.setting.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.setting(staff).font_size = -3

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            fontSize = #-3
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
    )

    assert abjad.inspect(staff).wellformed()


def test_LilyPondSettingNameManager___setattr___06():
    """
    Define LilyPond instrumentName context abjad.setting.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.setting(staff).instrument_name = "Violini I"

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            instrumentName = #"Violini I"
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
    )

    assert abjad.inspect(staff).wellformed()


def test_LilyPondSettingNameManager___setattr___07():
    """
    Define LilyPond instrumentName context abjad.setting.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.setting(staff).instrument_name = abjad.Markup(r"\circle { V }")

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            instrumentName = \markup {
                \circle
                    {
                        V
                    }
                }
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
    )

    assert abjad.inspect(staff).wellformed()


def test_LilyPondSettingNameManager___setattr___08():
    """
    Define LilyPond proportionalNotationDuration context abjad.setting.
    """

    score = abjad.Score([abjad.Staff("c'8 d'8 e'8 f'8")])
    moment = abjad.SchemeMoment(abjad.Fraction(1, 56))
    abjad.setting(score).proportional_notation_duration = moment

    assert format(score) == abjad.String.normalize(
        r"""
        \new Score
        \with
        {
            proportionalNotationDuration = #(ly:make-moment 1 56)
        }
        <<
            \new Staff
            {
                c'8
                d'8
                e'8
                f'8
            }
        >>
        """
    )

    assert abjad.inspect(score).wellformed()


def test_LilyPondSettingNameManager___setattr___09():
    """
    Define LilyPond shortInstrumentName context abjad.setting.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.setting(staff).short_instrument_name = "Vni. I"

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            shortInstrumentName = #"Vni. I"
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
    )

    assert abjad.inspect(staff).wellformed()


def test_LilyPondSettingNameManager___setattr___10():
    """
    Define LilyPond shortInstrumentName context abjad.setting.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.setting(staff).short_instrument_name = abjad.Markup(r"\circle { V }")

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            shortInstrumentName = \markup {
                \circle
                    {
                        V
                    }
                }
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
    )

    assert abjad.inspect(staff).wellformed()


def test_LilyPondSettingNameManager___setattr___11():
    """
    Define LilyPond suggestAccidentals context abjad.setting.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.setting(staff).suggest_accidentals = True

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            suggestAccidentals = ##t
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
    )

    assert abjad.inspect(staff).wellformed()


def test_LilyPondSettingNameManager___setattr___12():
    """
    Define LilyPond suggestAccidentals context abjad.setting.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.setting(staff[1]).suggest_accidentals = True

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            \set suggestAccidentals = ##t
            d'8
            e'8
            f'8
        }
        """
    )

    assert abjad.inspect(staff).wellformed()


def test_LilyPondSettingNameManager___setattr___13():
    """
    Define LilyPond tupletFullLength context abjad.setting.
    """

    staff = abjad.Staff([])
    abjad.setting(staff).tuplet_full_length = True

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            tupletFullLength = ##t
        }
        {
        }
        """
    )

    assert not len(staff)

    abjad.setting(staff).tuplet_full_length = False

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            tupletFullLength = ##f
        }
        {
        }
        """
    )

    assert not len(staff)

    del abjad.setting(staff).tuplet_full_length

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
        }
        """
    )

    assert not len(staff)
