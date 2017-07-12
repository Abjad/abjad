# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Component__remove_and_shrink_durated_parent_containers_01():
    r'''Remove leaf from container.
    '''

    container = abjad.Container("c'4 c'4 c'4 c'4 c'4 c'4")

    container[0]._remove_and_shrink_durated_parent_containers()

    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'4
            c'4
            c'4
            c'4
            c'4
        }
        '''
        )

    assert abjad.inspect(container).is_well_formed()


def test_scoretools_Component__remove_and_shrink_durated_parent_containers_02():
    r'''Remove leaf from voice.
    '''

    voice = abjad.Voice(6 * abjad.Note("c'4"))

    voice[0]._remove_and_shrink_durated_parent_containers()

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'4
            c'4
            c'4
            c'4
            c'4
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()


def test_scoretools_Component__remove_and_shrink_durated_parent_containers_03():
    r'''Remove leaf from staff.
    '''

    staff = abjad.Staff(abjad.Note("c'4") * 6)

    staff[0]._remove_and_shrink_durated_parent_containers()

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'4
            c'4
            c'4
            c'4
            c'4
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Component__remove_and_shrink_durated_parent_containers_04():
    r'''Remove leaf from tuplet.
    '''

    tuplet = abjad.Tuplet(abjad.Multiplier(4, 5), "c'8 d'8 e'8 f'8 g'8")

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \times 4/5 {
            c'8
            d'8
            e'8
            f'8
            g'8
        }
        '''
        )

    tuplet[0]._remove_and_shrink_durated_parent_containers()

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak edge-height #'(0.7 . 0)
        \times 4/5 {
            d'8
            e'8
            f'8
            g'8
        }
        '''
        )

    assert abjad.inspect(tuplet).is_well_formed()


def test_scoretools_Component__remove_and_shrink_durated_parent_containers_05():
    r'''Remove leaf from nested tuplet.
    '''

    tuplet = abjad.Tuplet(abjad.Multiplier(2, 3), [])
    tuplet.extend(r"c'2 cs'2 \times 2/3 { d'4 ef'4 e'4 }")
    leaves = abjad.select(tuplet).by_leaf()

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \times 2/3 {
            c'2
            cs'2
            \times 2/3 {
                d'4
                ef'4
                e'4
            }
        }
        '''
        )

    leaves[-1]._remove_and_shrink_durated_parent_containers()

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak edge-height #'(0.7 . 0)
        \times 2/3 {
            c'2
            cs'2
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                d'4
                ef'4
            }
        }
        '''
        )

    assert abjad.inspect(tuplet).is_well_formed()
