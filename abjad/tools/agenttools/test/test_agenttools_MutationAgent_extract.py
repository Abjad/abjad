from abjad import *



def test_agenttools_MutationAgent_extract_01():
    r'''Extracts note.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:])
    glissando = spannertools.Glissando()
    attach(glissando, voice[:])

    assert systemtools.TestManager.compare(
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

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            c'8 [ \glissando
            e'8 \glissando
            f'8 ]
        }
        '''
        )

    assert inspect_(note).is_well_formed()
    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_extract_02():
    r'''Extracts multiple notes.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:])
    glissando = spannertools.Glissando()
    attach(glissando, voice[:])

    assert systemtools.TestManager.compare(
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

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            e'8 [ \glissando
            f'8 ]
        }
        '''
        )

    for note in notes:
        assert inspect_(note).is_well_formed()

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_extract_03():
    r'''Extracts container.
    '''

    staff = Staff()
    staff.append(Container("c'8 d'8"))
    staff.append(Container("e'8 f'8"))
    beam = Beam()
    attach(beam, staff.select_leaves())

    assert systemtools.TestManager.compare(
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

    assert systemtools.TestManager.compare(
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
    assert inspect_(staff).is_well_formed()


def test_agenttools_MutationAgent_extract_04():
    r'''Extracts multiple containers.
    '''

    voice = Voice()
    voice.append(Container("c'8 d'8"))
    voice.append(Container("e'8 f'8"))
    voice.append(Container("g'8 a'8"))
    beam = Beam()
    attach(beam, voice.select_leaves())
    glissando = spannertools.Glissando()
    attach(glissando, voice.select_leaves())

    assert systemtools.TestManager.compare(
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

    assert systemtools.TestManager.compare(
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

    assert inspect_(voice).is_well_formed()
