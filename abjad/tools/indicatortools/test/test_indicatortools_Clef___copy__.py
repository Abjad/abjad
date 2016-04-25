# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_Clef___copy___01():
    r'''Copies explicit clefs copy.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    clef = Clef('treble')
    attach(clef, staff[0])
    clef = Clef('bass')
    attach(clef, staff[4])
    copied_notes = mutate(staff[:2]).copy()
    staff.extend(copied_notes)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \clef "treble"
            c'8
            cs'8
            d'8
            ef'8
            \clef "bass"
            e'8
            f'8
            fs'8
            g'8
            \clef "treble"
            c'8
            cs'8
        }
        ''')

    assert inspect_(staff).is_well_formed()
    assert inspect_(staff[0]).get_effective(Clef) == Clef('treble')
    assert inspect_(staff[1]).get_effective(Clef) == Clef('treble')
    assert inspect_(staff[2]).get_effective(Clef) == Clef('treble')
    assert inspect_(staff[3]).get_effective(Clef) == Clef('treble')
    assert inspect_(staff[4]).get_effective(Clef) == Clef('bass')
    assert inspect_(staff[5]).get_effective(Clef) == Clef('bass')
    assert inspect_(staff[6]).get_effective(Clef) == Clef('bass')
    assert inspect_(staff[7]).get_effective(Clef) == Clef('bass')
    assert inspect_(staff[8]).get_effective(Clef) == Clef('treble')
    assert inspect_(staff[9]).get_effective(Clef) == Clef('treble')


def test_indicatortools_Clef___copy___02():
    r'''Does not copy implicit clefs.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    clef = Clef('treble')
    attach(clef, staff[0])
    clef = Clef('bass')
    attach(clef, staff[4])
    copied_notes = mutate(staff[2:4]).copy()
    staff.extend(copied_notes)

    assert inspect_(staff).is_well_formed()
    assert inspect_(staff[0]).get_effective(Clef) == Clef('treble')
    assert inspect_(staff[1]).get_effective(Clef) == Clef('treble')
    assert inspect_(staff[2]).get_effective(Clef) == Clef('treble')
    assert inspect_(staff[3]).get_effective(Clef) == Clef('treble')
    assert inspect_(staff[4]).get_effective(Clef) == Clef('bass')
    assert inspect_(staff[5]).get_effective(Clef) == Clef('bass')
    assert inspect_(staff[6]).get_effective(Clef) == Clef('bass')
    assert inspect_(staff[7]).get_effective(Clef) == Clef('bass')
    assert inspect_(staff[8]).get_effective(Clef) == Clef('bass')
    assert inspect_(staff[9]).get_effective(Clef) == Clef('bass')

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \clef "treble"
            c'8
            cs'8
            d'8
            ef'8
            \clef "bass"
            e'8
            f'8
            fs'8
            g'8
            d'8
            ef'8
        }
        ''')
