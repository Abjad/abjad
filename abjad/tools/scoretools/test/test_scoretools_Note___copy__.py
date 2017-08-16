import abjad
import copy


def test_scoretools_Note___copy___01():
    r'''Copy note.
    '''

    note_1 = abjad.Note(12, (1, 4))
    note_2 = copy.copy(note_1)

    assert isinstance(note_1, abjad.Note)
    assert isinstance(note_2, abjad.Note)
    assert format(note_1) == format(note_2)
    assert note_1 is not note_2


def test_scoretools_Note___copy___02():
    r'''Copy note with LilyPond multiplier.
    '''

    note_1 = abjad.Note("c''4")
    abjad.attach(abjad.Multiplier(1, 2), note_1)
    note_2 = copy.copy(note_1)

    assert isinstance(note_1, abjad.Note)
    assert isinstance(note_2, abjad.Note)
    assert format(note_1) == format(note_2)
    assert note_1 is not note_2


def test_scoretools_Note___copy___03():
    r'''Copy note with LilyPond grob abjad.overrides and LilyPond context abjad.settings.
    '''

    note_1 = abjad.Note(12, (1, 4))
    abjad.override(note_1).staff.note_head.color = 'red'
    abjad.override(note_1).accidental.color = 'red'
    abjad.setting(note_1).tuplet_full_length = True
    note_2 = copy.copy(note_1)

    assert isinstance(note_1, abjad.Note)
    assert isinstance(note_2, abjad.Note)
    assert format(note_1) == format(note_2)
    assert note_1 is not note_2


def test_scoretools_Note___copy___04():
    r'''Copy note with grace container.
    '''

    note_1 = abjad.Note("c'4")
    grace_container_1 = abjad.AfterGraceContainer([abjad.Note("d'32")])
    abjad.attach(grace_container_1, note_1)

    assert format(note_1) == abjad.String.normalize(
        r'''
        \afterGrace
        c'4
        {
            d'32
        }
        '''
        )

    note_2 = copy.copy(note_1)
    grace_container_2 = abjad.inspect(note_2).get_after_grace_container()

    assert format(note_2) == abjad.String.normalize(
        r'''
        \afterGrace
        c'4
        {
            d'32
        }
        '''
        )

    assert note_1 is not note_2
    assert grace_container_1 is not grace_container_2
    assert isinstance(grace_container_1, abjad.AfterGraceContainer)



def test_scoretools_Note___copy___05():
    r'''Deepcopy orphan note.
    '''

    note = abjad.Note("c'4")
    articulation = abjad.Articulation('staccato')
    abjad.attach(articulation, note)
    grace = abjad.GraceContainer("d'16")
    abjad.attach(grace, note)
    abjad.override(note).note_head.color = 'red'

    assert format(note) == abjad.String.normalize(
        r'''
        \grace {
            d'16
        }
        \once \override NoteHead.color = #red
        c'4 -\staccato
        '''
        )

    new_note = copy.deepcopy(note)

    assert not new_note is note
    assert format(new_note) == format(note)


def test_scoretools_Note___copy___06():
    r'''Deepcopy note in score.
    '''

    staff = abjad.Staff("c'8 [ c'8 e'8 f'8 ]")
    note = staff[0]
    articulation = abjad.Articulation('staccato')
    abjad.attach(articulation, note)
    grace = abjad.GraceContainer("d'16")
    abjad.attach(grace, note)
    abjad.override(note).note_head.color = 'red'

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \grace {
                d'16
            }
            \once \override NoteHead.color = #red
            c'8 -\staccato [
            c'8
            e'8
            f'8 ]
        }
        '''
        )

    new_note = copy.deepcopy(note)

    assert new_note is not note
    assert abjad.inspect(note).get_parentage().parent is staff
    assert abjad.inspect(new_note).get_parentage().parent is not staff
    assert isinstance(abjad.inspect(new_note).get_parentage().parent, abjad.Staff)
    assert format(new_note) == format(note)
    assert format(abjad.inspect(note).get_parentage().parent) == \
        format(abjad.inspect(new_note).get_parentage().parent)


def test_scoretools_Note___copy___07():
    r'''Copying note does note copy hairpin.
    '''

    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(8)])
    crescendo = abjad.Hairpin('<')
    abjad.attach(crescendo, staff[:4])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 \<
            cs'8
            d'8
            ef'8 \!
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    new_note = copy.copy(staff[0])
    staff.append(new_note)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 \<
            cs'8
            d'8
            ef'8 \!
            e'8
            f'8
            fs'8
            g'8
            c'8
        }
        '''
        )
    assert abjad.inspect(staff).is_well_formed()
