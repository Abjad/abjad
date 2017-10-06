import abjad


def test_scoretools_Inspection_get_indicators_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    slur = abjad.Slur()
    abjad.attach(slur, staff[:])
    command_1 = abjad.LilyPondCommand('slurDotted')
    abjad.attach(command_1, staff[0])
    command_2 = abjad.LilyPondCommand('slurUp')
    abjad.attach(command_2, staff[0])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \slurDotted
            \slurUp
            c'8 (
            d'8
            e'8
            f'8 )
        }
        '''
        ), format(staff)

    indicators = abjad.inspect(staff[0]).get_indicators(abjad.LilyPondCommand)
    assert command_1 in indicators
    assert command_2 in indicators
    assert len(indicators) == 2


def test_scoretools_Inspection_get_indicators_02():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    slur = abjad.Slur()
    abjad.attach(slur, staff[:])
    comment = abjad.LilyPondComment('beginning of note content')
    abjad.attach(comment, staff[0])
    command = abjad.LilyPondCommand('slurDotted')
    abjad.attach(command, staff[0])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            % beginning of note content
            \slurDotted
            c'8 (
            d'8
            e'8
            f'8 )
        }
        '''
        ), format(staff)

    items = abjad.inspect(staff[0]).get_indicators()
    assert comment in items
    assert command in items
    assert len(items) == 2


def test_scoretools_Inspection_get_indicators_03():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    clef = abjad.Clef('treble')
    abjad.attach(clef, staff[0])
    dynamic = abjad.Dynamic('p')
    abjad.attach(dynamic, staff[0])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \clef "treble"
            c'8 \p
            d'8
            e'8
            f'8
        }
        '''
        ), format(staff)

    indicators = abjad.inspect(staff[0]).get_indicators()
    assert len(indicators) == 2


def test_scoretools_Inspection_get_indicators_04():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    comment_1 = abjad.LilyPondComment('comment 1')
    abjad.attach(comment_1, staff[0])
    comment_2 = abjad.LilyPondComment('comment 2')
    abjad.attach(comment_2, staff[0])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            % comment 1
            % comment 2
            c'8
            d'8
            e'8
            f'8
        }
        '''
        ), format(staff)

    indicators = abjad.inspect(staff[0]).get_indicators(abjad.LilyPondComment)
    assert comment_1 in indicators
    assert comment_2 in indicators
    assert len(indicators) == 2


def test_scoretools_Inspection_get_indicators_05():

    note = abjad.Note("c'4")
    stem_tremolo = abjad.StemTremolo(16)
    abjad.attach(stem_tremolo, note)
    stem_tremolos = abjad.inspect(note).get_indicators(abjad.StemTremolo)

    assert stem_tremolos[0] is stem_tremolo
