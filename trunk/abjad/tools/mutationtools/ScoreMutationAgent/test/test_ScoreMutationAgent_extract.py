from abjad import *



def test_ScoreMutationAgent_extract_01():
    r'''Extract note.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])
    spannertools.GlissandoSpanner(voice[:])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [ \glissando
            d'8 \glissando
            e'8 \glissando
            f'8 ]
        }
        '''
        )

    note = voice[1]
    mutate(note).extract()

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [ \glissando
            e'8 \glissando
            f'8 ]
        }
        '''
        )

    assert inspect(note).is_well_formed()
    assert inspect(voice).is_well_formed()


def test_ScoreMutationAgent_extract_02():
    r'''Extract multiple notes.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])
    spannertools.GlissandoSpanner(voice[:])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [ \glissando
            d'8 \glissando
            e'8 \glissando
            f'8 ]
        }
        '''
        )

    notes = voice[:2]
    for note in notes:
        mutate(note).extract()

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            e'8 [ \glissando
            f'8 ]
        }
        '''
        )

    for note in notes:
        assert inspect(note).is_well_formed()

    assert inspect(voice).is_well_formed()


def test_ScoreMutationAgent_extract_03():
    r'''Extract container.
    '''

    staff = Staff()
    staff.append(Container("c'8 d'8"))
    staff.append(Container("e'8 f'8"))
    beam = spannertools.BeamSpanner()
    beam.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                c'8 [
                d'8
            }
            {
                e'8
                f'8 ]
            }
        }
        '''
        )

    container = staff[0]
    mutate(container).extract()

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            d'8
            {
                e'8
                f'8 ]
            }
        }
        '''
        )

    assert not container
    assert inspect(staff).is_well_formed()


def test_ScoreMutationAgent_extract_04():
    r'''Extract multiple containers.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    voice = Voice()
    voice.append(Container("c'8 d'8"))
    voice.append(Container("e'8 f'8"))
    voice.append(Container("g'8 a'8"))
    spannertools.BeamSpanner(voice.select_leaves())
    spannertools.GlissandoSpanner(voice.select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            {
                e'8 \glissando
                f'8 \glissando
            }
            {
                g'8 \glissando
                a'8 ]
            }
        }
        '''
        )

    containers = voice[:2]
    for container in containers:
        mutate(container).extract()

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [ \glissando
            d'8 \glissando
            e'8 \glissando
            f'8 \glissando
            {
                g'8 \glissando
                a'8 ]
            }
        }
        '''
        )

    for container in containers:
        assert not container

    assert inspect(voice).is_well_formed()
