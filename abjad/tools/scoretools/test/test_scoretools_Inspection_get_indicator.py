import abjad
import pytest


def test_scoretools_Inspection_get_indicator_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.attach('color', staff[0])

    assert abjad.inspect(staff).get_indicator('color') is None
    assert abjad.inspect(staff[0]).get_indicator('color') == 'color'
    assert abjad.inspect(staff[1]).get_indicator('color') is None
    assert abjad.inspect(staff[2]).get_indicator('color') is None
    assert abjad.inspect(staff[3]).get_indicator('color') is None


def test_scoretools_Inspection_get_indicator_02():

    note = abjad.Note("c'8")
    articulation = abjad.Articulation('staccato')
    abjad.attach(articulation, note)

    assert abjad.inspect(note).get_indicator(abjad.Articulation) is articulation


def test_scoretools_Inspection_get_indicator_03():

    note = abjad.Note("c'8")

    assert abjad.inspect(note).get_indicator(abjad.Articulation) is None


def test_scoretools_Inspection_get_indicator_04():

    note = abjad.Note("c'8")
    articulation = abjad.Articulation('staccato')
    abjad.attach(articulation, note)
    articulation = abjad.Articulation('marcato')
    abjad.attach(articulation, note)

    statement = 'inspect(note).get_indicator(abjad.Articulation)'
    assert pytest.raises(Exception, statement)


def test_scoretools_Inspection_get_indicator_05():

    note = abjad.Note("c'8")
    command = abjad.LilyPondLiteral(r'\stemUp')
    abjad.attach(command, note)

    result = abjad.inspect(note).get_indicator(abjad.LilyPondLiteral)
    assert result is command


def test_scoretools_Inspection_get_indicator_06():

    note = abjad.Note("c'8")

    assert abjad.inspect(note).get_indicator(abjad.LilyPondLiteral) is None


def test_scoretools_Inspection_get_indicator_07():

    note = abjad.Note("c'8")
    command = abjad.LilyPondLiteral(r'\stemUp')
    abjad.attach(command, note)
    command = abjad.LilyPondLiteral(r'\slurUp')
    abjad.attach(command, note)

    statement = 'inspect(note).get_indicator(abjad.LilyPondLiteral)'
    assert pytest.raises(Exception, statement)


def test_scoretools_Inspection_get_indicator_08():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    slur = abjad.Slur()
    abjad.attach(slur, staff[:])
    command_1 = abjad.LilyPondLiteral(r'\slurDotted')
    abjad.attach(command_1, staff[0])
    command_2 = abjad.LilyPondLiteral(r'\slurUp')
    abjad.attach(command_2, staff[0])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            \slurDotted
            \slurUp
            c'8
            (
            d'8
            e'8
            f'8
            )
        }
        '''
        )

    indicators = abjad.inspect(staff[0]).get_indicators(abjad.LilyPondLiteral)

    assert command_1 in indicators
    assert command_2 in indicators
    assert len(indicators) == 2


def test_scoretools_Inspection_get_indicator_09():

    note = abjad.Note("c'8")
    comment = abjad.LilyPondComment('comment')
    abjad.attach(comment, note)

    indicator = abjad.inspect(note).get_indicator(abjad.LilyPondComment)
    assert indicator is comment


def test_scoretools_Inspection_get_indicator_10():

    note = abjad.Note("c'8")

    assert abjad.inspect(note).get_indicator(abjad.LilyPondComment) is None


def test_scoretools_Inspection_get_indicator_11():

    note = abjad.Note("c'8")
    comment = abjad.LilyPondComment('comment')
    abjad.attach(comment, note)
    comment = abjad.LilyPondComment('another comment')
    abjad.attach(comment, note)

    statement = 'inspect(note).get_indicator(abjad.LilyPondComment)'
    assert pytest.raises(Exception, statement)


def test_scoretools_Inspection_get_indicator_12():

    note = abjad.Note("c'8")

    assert abjad.inspect(note).get_indicator() is None


def test_scoretools_Inspection_get_indicator_13():

    note = abjad.Note("c'4")
    stem_tremolo = abjad.StemTremolo(16)
    abjad.attach(stem_tremolo, note)
    stem_tremolo = abjad.inspect(note).get_indicator(abjad.StemTremolo)

    assert stem_tremolo is stem_tremolo


def test_scoretools_Inspection_get_indicator_14():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    violin = abjad.Violin()
    abjad.attach(violin, staff[0])

    indicator = abjad.inspect(staff[0]).get_indicator(abjad.Instrument)

    assert indicator is violin


def test_scoretools_Inspection_get_indicator_15():

    measure = abjad.Measure((4, 8), "c'8 d'8 e'8 f'8")
    indicator = abjad.inspect(measure).get_indicator(abjad.TimeSignature)

    assert indicator == abjad.TimeSignature((4, 8))
