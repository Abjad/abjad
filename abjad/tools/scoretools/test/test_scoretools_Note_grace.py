import abjad


def test_scoretools_Note_grace_01():
    r'''Attaches one grace note.
    '''

    note = abjad.Note("c'4")
    grace_container = abjad.GraceContainer([abjad.Note(2, (1, 16))])
    abjad.attach(grace_container, note)

    assert format(note) == abjad.String.normalize(
        r'''
        \grace {
            d'16
        }
        c'4
        '''
        )


def test_scoretools_Note_grace_02():
    r'''Attaches several grace notes.
    '''

    note = abjad.Note("c'4")
    grace_notes = [abjad.Note(0, (1, 16)), abjad.Note(2, (1, 16)), abjad.Note(4, (1, 16))]
    grace_container = abjad.GraceContainer(grace_notes)
    abjad.attach(grace_container, note)

    assert format(note) == abjad.String.normalize(
        r'''
        \grace {
            c'16
            d'16
            e'16
        }
        c'4
        '''
        )


def test_scoretools_Note_grace_03():
    r'''Attaches one appoggiatura.
    '''

    note = abjad.Note("c'4")
    grace_container = abjad.AppoggiaturaContainer([abjad.Note(2, (1, 16))])
    abjad.attach(grace_container, note)

    assert format(note) == abjad.String.normalize(
        r'''
        \appoggiatura {
            d'16
        }
        c'4
        '''
        )


def test_scoretools_Note_grace_04():
    r'''Attaches one acciaccatura.
    '''

    note = abjad.Note("c'4")
    grace = abjad.AcciaccaturaContainer([abjad.Note(2, (1, 16))])
    abjad.attach(grace, note)

    assert format(note) == abjad.String.normalize(
        r'''
        \acciaccatura {
            d'16
        }
        c'4
        '''
        )


def test_scoretools_Note_grace_05():
    r'''Attaches one after grace note.
    '''

    note = abjad.Note("c'4")
    grace = abjad.AfterGraceContainer([abjad.Note(2, (1, 16))])
    abjad.attach(grace, note)

    assert format(note) == abjad.String.normalize(
        r'''
        \afterGrace
        c'4
        {
            d'16
        }
        '''
        )


def test_scoretools_Note_grace_06():
    r'''Attaches several after grace notes.
    '''

    note = abjad.Note("c'4")
    grace_notes = [abjad.Note(0, (1, 16)), abjad.Note(2, (1, 16)), abjad.Note(4, (1, 16))]
    grace = abjad.AfterGraceContainer(grace_notes)
    abjad.attach(grace, note)

    assert format(note) == abjad.String.normalize(
        r'''
        \afterGrace
        c'4
        {
            c'16
            d'16
            e'16
        }
        '''
        )
