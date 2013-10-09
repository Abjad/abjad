# -*- encoding: utf-8 -*-
from abjad import *


def test_LilyPondContextSettingComponentPlugIn___setattr___01():
    r'''Define LilyPond autoBeaming context setting.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.set.auto_beaming = True

    r'''
    \new Staff \with {
        autoBeaming = ##t
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff \with {
            autoBeaming = ##t
        } {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )


def test_LilyPondContextSettingComponentPlugIn___setattr___02():
    r'''Remove LilyPond autoBeaming context setting.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.set.auto_beaming = True
    del(staff.set.auto_beaming)

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )


def test_LilyPondContextSettingComponentPlugIn___setattr___03():
    r'''Define LilyPond currentBarNumber context setting.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff[0].set.score.current_bar_number = 12

    r'''
    \new Staff {
        \set Score.currentBarNumber = #12
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \set Score.currentBarNumber = #12
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )


def test_LilyPondContextSettingComponentPlugIn___setattr___04():
    r'''Define LilyPond currentBarNumber context setting.
    '''

    staff = Staff()
    staff.append(Measure((2, 8), "c'8 d'8"))
    staff.append(Measure((2, 8), "e'8 f'8"))
    staff[0].set.score.current_bar_number = 12

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \set Score.currentBarNumber = #12
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_LilyPondContextSettingComponentPlugIn___setattr___05():
    r'''Define LilyPond fontSize context setting.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.set.font_size = -3

    assert testtools.compare(
        staff,
        r'''
        \new Staff \with {
            fontSize = #-3
        } {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_LilyPondContextSettingComponentPlugIn___setattr___06():
    r'''Define LilyPond instrumentName context setting.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.set.instrument_name = 'Violini I'

    assert testtools.compare(
        staff,
        r'''
        \new Staff \with {
            instrumentName = "Violini I"
        } {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_LilyPondContextSettingComponentPlugIn___setattr___07():
    r'''Define LilyPond instrumentName context setting.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.set.instrument_name = markuptools.Markup(r'\circle { V }')

    assert testtools.compare(
        staff,
        r'''
        \new Staff \with {
            instrumentName = \markup { \circle { V } }
        } {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_LilyPondContextSettingComponentPlugIn___setattr___08():
    r'''Define LilyPond proportionalNotationDuration context setting.
    '''

    score = Score([Staff("c'8 d'8 e'8 f'8")])
    score.set.proportional_notation_duration = \
        schemetools.SchemeMoment(Fraction(1, 56))

    assert testtools.compare(
        score,
        r'''
        \new Score \with {
            proportionalNotationDuration = #(ly:make-moment 1 56)
        } <<
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
        >>
        '''
        )

    assert inspect(score).is_well_formed()


def test_LilyPondContextSettingComponentPlugIn___setattr___09():
    r'''Define LilyPond shortInstrumentName context setting.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.set.short_instrument_name = 'Vni. I'

    assert testtools.compare(
        staff,
        r'''
        \new Staff \with {
            shortInstrumentName = "Vni. I"
        } {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_LilyPondContextSettingComponentPlugIn___setattr___10():
    r'''Define LilyPond shortInstrumentName context setting.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.set.short_instrument_name = markuptools.Markup(r'\circle { V }')

    assert testtools.compare(
        staff,
        r'''
        \new Staff \with {
            shortInstrumentName = \markup { \circle { V } }
        } {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_LilyPondContextSettingComponentPlugIn___setattr___11():
    r'''Define LilyPond suggestAccidentals context setting.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.set.suggest_accidentals = True

    assert testtools.compare(
        staff,
        r'''
        \new Staff \with {
            suggestAccidentals = ##t
        } {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_LilyPondContextSettingComponentPlugIn___setattr___12():
    r'''Define LilyPond suggestAccidentals context setting.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff[1].set.suggest_accidentals = True

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            \set suggestAccidentals = ##t
            d'8
            e'8
            f'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_LilyPondContextSettingComponentPlugIn___setattr___13():
    r'''Define LilyPond tupletFullLength context setting.
    '''

    staff = Staff([])
    staff.set.tuplet_full_length = True

    assert testtools.compare(
        staff,
        r'''
        \new Staff \with {
            tupletFullLength = ##t
        } {
        }
        '''
        )

    assert inspect(staff).is_well_formed()

    staff.set.tuplet_full_length = False

    assert testtools.compare(
        staff,
        r'''
        \new Staff \with {
            tupletFullLength = ##f
        } {
        }
        '''
        )

    assert inspect(staff).is_well_formed()

    del(staff.set.tuplet_full_length)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
        }
        '''
        )

    assert inspect(staff).is_well_formed()
