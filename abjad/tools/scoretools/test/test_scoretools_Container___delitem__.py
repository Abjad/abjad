# -*- encoding: utf-8 -*-
from abjad import *



def test_scoretools_Container___delitem___01():
    r'''Delete spanned component.
    Component withdraws crossing spanners.
    Component carries covered spanners forward.
    Operation always leaves all expressions in tact.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 }")
    beam = Beam()
    attach(beam, voice[:])
    slur = Slur()
    attach(slur, voice[0][:])
    slur = Slur()
    attach(slur, voice[1][:])

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ (
                d'8 )
            }
            {
                e'8 (
                f'8 ] )
            }
        }
        '''
        )

    old = voice[0]
    del(voice[0])

    "Container voice is now ..."

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            {
                e'8 [ (
                f'8 ] )
            }
        }
        '''
        )

    assert inspect_(voice).is_well_formed()

    "Deleted component is now ..."

    assert systemtools.TestManager.compare(
        old,
        r'''
        {
            c'8 (
            d'8 )
        }
        '''
        )

    assert inspect_(old).is_well_formed()


def test_scoretools_Container___delitem___02():
    r'''Delete 1 leaf in container.
    Spanner structure is preserved.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:])

    del(voice[1])

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            e'8
            f'8 ]
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___delitem___03():
    r'''Delete slice in middle of container.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:])

    del(voice[1:3])

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            f'8 ]
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___delitem___04():
    r'''Delete slice from beginning to middle of container.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:])

    del(voice[:2])

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            e'8 [
            f'8 ]
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___delitem___05():
    r'''Delete slice from middle to end of container.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:])

    del(voice[2:])

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            d'8 ]
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___delitem___06():
    r'''Delete slice from beginning to end of container.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:])

    del(voice[:])

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___delitem___07():
    r'''Delete leaf from tuplet.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    beam = Beam()
    attach(beam, tuplet[:])

    del(tuplet[1])

    assert systemtools.TestManager.compare(
        tuplet,
        r'''
        {
            c'8 [
            e'8 ]
        }
        '''
        )

    assert inspect_(tuplet).is_well_formed()


def test_scoretools_Container___delitem___08():
    r'''Delete leaf from nested container.
    '''

    voice = Voice("c'8 { d'8 e'8 } f'8")
    beam = Beam()
    attach(beam, voice.select_leaves())
    glissando = spannertools.Glissando()
    attach(glissando, voice.select_leaves())

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            c'8 [ \glissando
            {
                d'8 \glissando
                e'8 \glissando
            }
            f'8 ]
        }
        '''
        )

    leaf = voice.select_leaves()[1]
    del(voice[1][0])

    assert systemtools.TestManager.compare(
        voice,
        r'''
        \new Voice {
            c'8 [ \glissando
            {
                e'8 \glissando
            }
            f'8 ]
        }
        '''
        )

    assert inspect_(voice).is_well_formed()
    assert inspect_(leaf).is_well_formed()
