from abjad import *


def test_LilyPondContextSettingComponentPlugIn___setattr___01():
    '''Define LilyPond autoBeaming context setting.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.set.auto_beaming = True

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff \\with {\n\tautoBeaming = ##t\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondContextSettingComponentPlugIn___setattr___02():
    '''Remove LilyPond autoBeaming context setting.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.set.auto_beaming = True
    del(t.set.auto_beaming)

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondContextSettingComponentPlugIn___setattr___03():
    '''Define LilyPond currentBarNumber context setting.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t[0].set.score.current_bar_number = 12

    r'''
    \new Staff {
        \set Score.currentBarNumber = #12
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t\\set Score.currentBarNumber = #12\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondContextSettingComponentPlugIn___setattr___04():
    '''Define LilyPond currentBarNumber context setting.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    t[0].set.score.current_bar_number = 12

    r'''
    \new Staff {
        {
            \set Score.currentBarNumber = #12
            \time 2/8
            c'8
            d'8
        }
        {
            \time 2/8
            e'8
            f'8
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t{\n\t\t\\set Score.currentBarNumber = #12\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t}\n}"

def test_LilyPondContextSettingComponentPlugIn___setattr___05():
    '''Define LilyPond fontSize context setting.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.set.font_size = -3

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff \\with {\n\tfontSize = #-3\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondContextSettingComponentPlugIn___setattr___06():
    '''Define LilyPond instrumentName context setting.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.set.instrument_name = 'Violini I'

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == '\\new Staff \\with {\n\tinstrumentName = "Violini I"\n} {\n\tc\'8\n\td\'8\n\te\'8\n\tf\'8\n}'


def test_LilyPondContextSettingComponentPlugIn___setattr___07():
    '''Define LilyPond instrumentName context setting.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.set.instrument_name = markuptools.Markup(r'\circle { V }')

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff \\with {\n\tinstrumentName = \\markup { \\circle { V } }\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondContextSettingComponentPlugIn___setattr___08():
    '''Define LilyPond proportionalNotationDuration context setting.
    '''

    t = Score([Staff("c'8 d'8 e'8 f'8")])
    t.set.proportional_notation_duration = schemetools.SchemeMoment(Fraction(1, 56))

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Score \\with {\n\tproportionalNotationDuration = #(ly:make-moment 1 56)\n} <<\n\t\\new Staff {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n>>"


def test_LilyPondContextSettingComponentPlugIn___setattr___09():
    '''Define LilyPond shortInstrumentName context setting.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.set.short_instrument_name = 'Vni. I'

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == '\\new Staff \\with {\n\tshortInstrumentName = "Vni. I"\n} {\n\tc\'8\n\td\'8\n\te\'8\n\tf\'8\n}'


def test_LilyPondContextSettingComponentPlugIn___setattr___10():
    '''Define LilyPond shortInstrumentName context setting.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.set.short_instrument_name = markuptools.Markup(r'\circle { V }')

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff \\with {\n\tshortInstrumentName = \\markup { \\circle { V } }\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondContextSettingComponentPlugIn___setattr___11():
    '''Define LilyPond suggestAccidentals context setting.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.set.suggest_accidentals = True

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff \\with {\n\tsuggestAccidentals = ##t\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondContextSettingComponentPlugIn___setattr___12():
    '''Define LilyPond suggestAccidentals context setting.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t[1].set.suggest_accidentals = True

    r'''
    \new Staff {
        c'8
        \set suggestAccidentals = ##t
        d'8
        e'8
        f'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8\n\t\\set suggestAccidentals = ##t\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondContextSettingComponentPlugIn___setattr___13():
    '''Define LilyPond tupletFullLength context setting.
    '''

    t = Staff([])
    #t.tuplet_bracket.tuplet_full_length = True
    t.set.tuplet_full_length = True

    r'''
    \new Staff \with {
        tupletFullLength = ##t
    } {
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == '\\new Staff \\with {\n\ttupletFullLength = ##t\n} {\n}'

    #t.tuplet_bracket.tuplet_full_length = False
    t.set.tuplet_full_length = False

    r'''
    \new Staff \with {
        tupletFullLength = ##f
    } {
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == '\\new Staff \\with {\n\ttupletFullLength = ##f\n} {\n}'

    #t.tuplet_bracket.tuplet_full_length = None
    del(t.set.tuplet_full_length)

    r'''
    \new Staff {
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == '\\new Staff {\n}'
