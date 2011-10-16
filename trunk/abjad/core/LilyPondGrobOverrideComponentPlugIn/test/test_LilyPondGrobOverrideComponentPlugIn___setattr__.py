from abjad import *
import py.test


def test_LilyPondGrobOverrideComponentPlugIn___setattr___01():
    '''Override LilyPond Accidental grob.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.override.accidental.color = 'red'

    r'''
    \new Staff \with {
        \override Accidental #'color = #red
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert t.format == "\\new Staff \\with {\n\t\\override Accidental #'color = #red\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___02():
    '''Override LilyPond Accidental grob.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t[1].override.accidental.color = 'red'

    r'''
    \new Staff {
        c'8
        \once \override Accidental #'color = #red
        d'8
        e'8
        f'8
    }
    '''

    assert t.format == "\\new Staff {\n\tc'8\n\t\\once \\override Accidental #'color = #red\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___03():
    '''Override LilyPond BarNumber grob.
    '''

    score = Score([Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    score.override.bar_number.break_visibility = schemetools.SchemeFunction('end-of-line-invisible')

    r'''
    \new Score \with {
        \override BarNumber #'break-visibility = #end-of-line-invisible
    } <<
        \new Staff {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
            b'8
            c''8
        }
    >>
    '''

    assert componenttools.is_well_formed_component(score)
    assert score.format == "\\new Score \\with {\n\t\\override BarNumber #'break-visibility = #end-of-line-invisible\n} <<\n\t\\new Staff {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t\tg'8\n\t\ta'8\n\t\tb'8\n\t\tc''8\n\t}\n>>"

def test_LilyPondGrobOverrideComponentPlugIn___setattr___04():
    '''Override LilyPond BarNumber grob.
    '''

    t = Score([Staff("c'8 d'8 e'8 f'8")])
    t.override.bar_number.color = 'red'

    r'''
    \new Score \with {
        \override BarNumber #'color = #red
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
    assert t.format == "\\new Score \\with {\n\t\\override BarNumber #'color = #red\n} <<\n\t\\new Staff {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n>>"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___05():
    '''Override LilyPond Beam grob.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    p = spannertools.BeamSpanner(t[:])
    p.override.beam.positions = (4, 4)

    r'''
    \new Voice {
        \override Beam #'positions = #'(4 . 4)
        c'8 [
        d'8
        e'8
        f'8 ]
        \revert Beam #'positions
    }
    '''

    assert t.format == "\\new Voice {\n\t\\override Beam #'positions = #'(4 . 4)\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n\t\\revert Beam #'positions\n}"

def test_LilyPondGrobOverrideComponentPlugIn___setattr___06():
    '''Override LilyPond Clef grob.
    '''

    t = Note("c'4")
    t.override.clef.color = 'red'

    r'''
    \once \override Clef #'color = #red
    c'4
    '''

    assert t.format == "\\once \\override Clef #'color = #red\nc'4"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___07():
    '''Override LilyPond Clef grob.
    '''

    t = Note("c'4")
    t.override.staff.clef.color = 'red'

    assert t.format == "\\once \\override Staff.Clef #'color = #red\nc'4"
    r'''
    \once \override Staff.Clef #'color = #red
    c'4
    '''


def test_LilyPondGrobOverrideComponentPlugIn___setattr___08():
    '''Override LilyPond Clef grob.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.override.clef.color = 'red'

    r'''
    \new Staff \with {
        \override Clef #'color = #red
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert t.format == "\\new Staff \\with {\n\t\\override Clef #'color = #red\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___09():
    '''Override LilyPond ClusterSpanner grob.
    '''

    t = containertools.Cluster(Note(1, (1, 4)) * 4)
    t.override.cluster_spanner.style = 'ramp'
    t.override.cluster_spanner.padding = 0.1

    r'''
    \makeClusters {
        \override ClusterSpanner #'padding = #0.1
        \override ClusterSpanner #'style = #'ramp
        cs'4
        cs'4
        cs'4
        cs'4
        \revert ClusterSpanner #'padding
        \revert ClusterSpanner #'style
    }
    '''

    assert t.format == "\\makeClusters {\n\t\\override ClusterSpanner #'padding = #0.1\n\t\\override ClusterSpanner #'style = #'ramp\n\tcs'4\n\tcs'4\n\tcs'4\n\tcs'4\n\t\\revert ClusterSpanner #'padding\n\t\\revert ClusterSpanner #'style\n}"

    del(t.override.cluster_spanner)

    r'''
    \makeClusters {
        cs'4
        cs'4
        cs'4
        cs'4
    }
    '''

    assert t.format == "\\makeClusters {\n\tcs'4\n\tcs'4\n\tcs'4\n\tcs'4\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___10():
    '''Override LilyPond DynamicLineSpanner grob.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    p = spannertools.HairpinSpanner(t[:], 'p < f')
    p.override.dynamic_line_spanner.staff_padding = 4

    r'''
    \new Voice {
        \override DynamicLineSpanner #'staff-padding = #4
        c'8 \< \p
        d'8
        e'8
        f'8 \f
        \revert DynamicLineSpanner #'staff-padding
    }
    '''

    assert t.format == "\\new Voice {\n\t\\override DynamicLineSpanner #'staff-padding = #4\n\tc'8 \\< \\p\n\td'8\n\te'8\n\tf'8 \\f\n\t\\revert DynamicLineSpanner #'staff-padding\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___11():
    '''Override LilyPond DynamicLineSpanner grob.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.override.dynamic_line_spanner.staff_padding = 2
    t.override.dynamic_line_spanner.Y_extent = (-1.5, 1.5)

    r'''
    \new Staff \with {
        \override DynamicLineSpanner #'Y-extent = #'(-1.5 . 1.5)
        \override DynamicLineSpanner #'staff-padding = #2
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert t.format == "\\new Staff \\with {\n\t\\override DynamicLineSpanner #'Y-extent = #'(-1.5 . 1.5)\n\t\\override DynamicLineSpanner #'staff-padding = #2\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___12():
    '''Override LilyPond DynamicText grob.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    p = spannertools.DynamicTextSpanner(t[:], 'f')
    p.override.dynamic_text.thickness = 3

    r'''
    \new Voice {
        \override DynamicText #'thickness = #3
        c'8 [ \f
        d'8
        e'8
        f'8 ]
        \revert DynamicText #'thickness
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t\\override DynamicText #'thickness = #3\n\tc'8 [ \\f\n\td'8\n\te'8\n\tf'8 ]\n\t\\revert DynamicText #'thickness\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___13():
    '''Override LilyPond DynamicText grob.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.override.dynamic_text.staff_padding = 2
    t.override.dynamic_text.Y_extent = (-1.5, 1.5)

    r'''
    \new Staff \with {
        \override DynamicText #'Y-extent = #'(-1.5 . 1.5)
        \override DynamicText #'staff-padding = #2
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert t.format == "\\new Staff \\with {\n\t\\override DynamicText #'Y-extent = #'(-1.5 . 1.5)\n\t\\override DynamicText #'staff-padding = #2\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___14():
    '''Override LilyPond DynamicTextSpanner grob.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.override.dynamic_text_spanner.staff_padding = 2
    t.override.dynamic_text_spanner.Y_extent = (-1.5, 1.5)

    r'''
    \new Staff \with {
        \override DynamicTextSpanner #'Y-extent = #'(-1.5 . 1.5)
        \override DynamicTextSpanner #'staff-padding = #2
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert t.format == "\\new Staff \\with {\n\t\\override DynamicTextSpanner #'Y-extent = #'(-1.5 . 1.5)\n\t\\override DynamicTextSpanner #'staff-padding = #2\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___15():
    '''Override LilyPond Glissando grob.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    p = spannertools.GlissandoSpanner(t[:])
    p.override.glissando.thickness = 3

    r'''
    \new Voice {
        \override Glissando #'thickness = #3
        c'8 \glissando
        d'8 \glissando
        e'8 \glissando
        f'8
        \revert Glissando #'thickness
    }
    '''

    assert t.format == "\\new Voice {\n\t\\override Glissando #'thickness = #3\n\tc'8 \\glissando\n\td'8 \\glissando\n\te'8 \\glissando\n\tf'8\n\t\\revert Glissando #'thickness\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___16():
    '''Override LilyPond Hairpin grob.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.override.hairpin.staff_padding = 2
    t.override.hairpin.Y_extent = (-1.5, 1.5)

    r'''
    \new Staff \with {
        \override Hairpin #'Y-extent = #'(-1.5 . 1.5)
        \override Hairpin #'staff-padding = #2
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert t.format == "\\new Staff \\with {\n\t\\override Hairpin #'Y-extent = #'(-1.5 . 1.5)\n\t\\override Hairpin #'staff-padding = #2\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___17():
    '''Override LilyPond InstrumentName grob.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.set.instrument_name = markuptools.Markup(r'\circle { V }')
    t.override.instrument_name.color = 'red'

    r'''
    \new Staff \with {
        \override InstrumentName #'color = #red
        instrumentName = \markup { \circle { V } }
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff \\with {\n\t\\override InstrumentName #'color = #red\n\tinstrumentName = \\markup { \\circle { V } }\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___18():
    '''Override LilyPond MetronomeMark grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    score = Score([staff])
    contexttools.TempoMark(Duration(1, 4), 58)(staff[0])
    score.override.metronome_mark.color = 'red'

    r'''
    \new Score \with {
        \override MetronomeMark #'color = #red
    } <<
        \new Staff {
            \tempo 4=58
            c'8
            d'8
            e'8
            f'8
        }
    >>
    '''

    assert componenttools.is_well_formed_component(score)
    assert score.format == "\\new Score \\with {\n\t\\override MetronomeMark #'color = #red\n} <<\n\t\\tempo 4=58\n\t\\new Staff {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n>>"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___19():
    '''Override LilyPond MultiMeasureRestGrob.
    '''

    staff = Staff([Note("c'4")])
    staff.override.multi_measure_rest.expand_limit = 12

    r'''
    \new Staff \with {
        \override MultiMeasureRest #'expand-limit = #12
    } {
        c'4
    }
    '''

    assert staff.format == "\\new Staff \\with {\n\t\\override MultiMeasureRest #'expand-limit = #12\n} {\n\tc'4\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___20():
    '''Override LilyPond NonMusicalPaperColumn grob.
    '''

    t = Score([Staff("c'8 d'8 e'8 f'8")])
    t.override.non_musical_paper_column.line_break_permission = False
    t.override.non_musical_paper_column.page_break_permission = False

    r'''
    \new Score \with {
        \override NonMusicalPaperColumn #'line-break-permission = ##f
        \override NonMusicalPaperColumn #'page-break-permission = ##f
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
    assert t.format == "\\new Score \\with {\n\t\\override NonMusicalPaperColumn #'line-break-permission = ##f\n\t\\override NonMusicalPaperColumn #'page-break-permission = ##f\n} <<\n\t\\new Staff {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n>>"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___21():
    '''Override LilyPond NoteColumn grob.
    '''

    t = Note("c'4")
    t.override.note_column.ignore_collision = True

    r'''
    \once \override NoteColumn #'ignore-collision = ##t
    c'4
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\once \\override NoteColumn #'ignore-collision = ##t\nc'4"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___22():
    '''Override LilyPond NoteColumn grob.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.override.note_column.ignore_collision = True

    r'''
    \new Staff \with {
        \override NoteColumn #'ignore-collision = ##t
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff \\with {\n\t\\override NoteColumn #'ignore-collision = ##t\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___23():
    '''Override LilyPond NoteHead grob.
    '''

    t = Note(1, (1, 4))
    t.override.note_head.style = 'cross'

    assert t.override.note_head.style == 'cross'
    assert t.format == "\\once \\override NoteHead #'style = #'cross\ncs'4"

    del(t.override.note_head.style)
    assert t.note_head.format == "cs'"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___24():
    '''Notehead styles are handled just like all other grob overrides.'''

    t = Note(1, (1, 4))
    t.override.note_head.style = 'mystrangehead'

    assert t.override.note_head.style == 'mystrangehead'
    assert t.format == "\\once \\override NoteHead #'style = #'mystrangehead\ncs'4"

    del(t.override.note_head.style)
    assert t.note_head.format == "cs'"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___25():
    '''Notehead style overrides are handled just like all other
    note_head grob overrides, even for note_heads in chords.'''

    t = Chord([1, 2, 3], (1, 4))
    t.note_heads[0].tweak.style = 'harmonic'

    r'''
    <
        \tweak #'style #'harmonic
        cs'
        d'
        ef'
    >4
    '''

    assert t.format == "<\n\t\\tweak #'style #'harmonic\n\tcs'\n\td'\n\tef'\n>4"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___26():
    '''Notehead shape style overrides are just normal grob overrides.'''

    t = Note(1, (1, 4))
    t.override.note_head.style = 'triangle'

    assert t.override.note_head.style == 'triangle'
    assert t.format == "\\once \\override NoteHead #'style = #'triangle\ncs'4"

    del(t.override.note_head.style)
    assert t.format == "cs'4"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___27():
    '''Notehead solfege style overrides are just normal grob overrides.
    Modern versions of LilyPond now handles solfege overrides correctly.'''

    t = Note(1, (1, 4))
    t.override.note_head.style = 'do'

    assert t.override.note_head.style == 'do'
    assert t.format == "\\once \\override NoteHead #'style = #'do\ncs'4"

    del(t.override.note_head.style)
    assert t.format == "cs'4"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___28():
    '''Override LilyPond NoteHead grob.
    '''

    t = Note(13, (1, 4))
    t.override.note_head.transparent = True

    assert t.override.note_head.transparent
    assert t.format == "\\once \\override NoteHead #'transparent = ##t\ncs''4"

    del(t.override.note_head.transparent)
    assert t.format == "cs''4"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___29():
    '''Override LilyPond NoteHead grob.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    t.override.note_head.color = 'red'

    r'''
    \new Voice \with {
        \override NoteHead #'color = #red
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice \\with {\n\t\\override NoteHead #'color = #red\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___30():
    '''Override LilyPond OctavationBracket grob.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    p = spannertools.OctavationSpanner(t[:], 1)
    p.override.staff.ottava_bracket.staff_position = 4

    r'''
    \new Voice {
        \override Staff.OttavaBracket #'staff-position = #4
        \ottava #1
        c'8
        d'8
        e'8
        f'8
        \ottava #0
        \revert Staff.OttavaBracket #'staff-position
    }
    '''

    assert t.format == "\\new Voice {\n\t\\override Staff.OttavaBracket #'staff-position = #4\n\t\\ottava #1\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\ottava #0\n\t\\revert Staff.OttavaBracket #'staff-position\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___31():
    '''Override LilyPond RehearsalMark grob.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.override.rehearsal_mark.staff_padding = 2
    t.override.rehearsal_mark.Y_extent = (-1.5, 1.5)

    r'''
    \new Staff \with {
        \override RehearsalMark #'Y-extent = #'(-1.5 . 1.5)
        \override RehearsalMark #'staff-padding = #2
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert t.format == "\\new Staff \\with {\n\t\\override RehearsalMark #'Y-extent = #'(-1.5 . 1.5)\n\t\\override RehearsalMark #'staff-padding = #2\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___32():
    '''Override LilyPond Rest grob.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.override.rest.transparent = True

    r'''
    \new Staff \with {
        \override Rest #'transparent = ##t
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert t.format == "\\new Staff \\with {\n\t\\override Rest #'transparent = ##t\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___33():
    '''Override LilyPond Script grob.
    '''

    t = Note("c'4")
    marktools.Articulation('staccato')(t)
    t.override.script.color = 'red'

    r'''
    \once \override Script #'color = #red
    c'4 -\staccato
    '''

    assert t.format == "\\once \\override Script #'color = #red\nc'4 -\\staccato"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___34():
    '''Override LilyPond Script grob.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.override.script.staff_padding = 2
    t.override.script.Y_extent = (-1.5, 1.5)

    r'''
    \new Staff \with {
        \override Script #'Y-extent = #'(-1.5 . 1.5)
        \override Script #'staff-padding = #2
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert t.format == "\\new Staff \\with {\n\t\\override Script #'Y-extent = #'(-1.5 . 1.5)\n\t\\override Script #'staff-padding = #2\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___35():
    '''Override LilyPond SpacingSpanner grob.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    p = spannertools.Spanner(t[:])
    p.override.score.spacing_spanner.strict_grace_spacing = True
    p.override.score.spacing_spanner.strict_note_spacing = True
    p.override.score.spacing_spanner.uniform_stretching = True

    r'''
    \new Staff {
        \override Score.SpacingSpanner #'strict-grace-spacing = ##t
        \override Score.SpacingSpanner #'strict-note-spacing = ##t
        \override Score.SpacingSpanner #'uniform-stretching = ##t
        c'8
        d'8
        e'8
        f'8
        \revert Score.SpacingSpanner #'strict-grace-spacing
        \revert Score.SpacingSpanner #'strict-note-spacing
        \revert Score.SpacingSpanner #'uniform-stretching
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t\\override Score.SpacingSpanner #'strict-grace-spacing = ##t\n\t\\override Score.SpacingSpanner #'strict-note-spacing = ##t\n\t\\override Score.SpacingSpanner #'uniform-stretching = ##t\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\revert Score.SpacingSpanner #'strict-grace-spacing\n\t\\revert Score.SpacingSpanner #'strict-note-spacing\n\t\\revert Score.SpacingSpanner #'uniform-stretching\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___36():
    '''Override LilyPond SpacingSpanner grob on Abjad containers.
    LilyPond SpacingSpanner lives at Score by default.
    Abjad SpacingSpanner overrides usually
    require context promotion.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    p = spannertools.Spanner(t[:])
    p.override.score.spacing_spanner.strict_grace_spacing = True
    p.override.score.spacing_spanner.strict_note_spacing = True
    p.override.score.spacing_spanner.uniform_stretching = True


    r'''
    \new Staff {
        {
            \time 2/8
            \override Score.SpacingSpanner #'strict-grace-spacing = ##t
            \override Score.SpacingSpanner #'strict-note-spacing = ##t
            \override Score.SpacingSpanner #'uniform-stretching = ##t
            c'8
            d'8
        }
        {
            \time 2/8
            e'8
            f'8
            \revert Score.SpacingSpanner #'strict-note-spacing
            \revert Score.SpacingSpanner #'strict-grace-spacing
            \revert Score.SpacingSpanner #'uniform-stretching
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\t\\override Score.SpacingSpanner #'strict-grace-spacing = ##t\n\t\t\\override Score.SpacingSpanner #'strict-note-spacing = ##t\n\t\t\\override Score.SpacingSpanner #'uniform-stretching = ##t\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t\t\\revert Score.SpacingSpanner #'strict-grace-spacing\n\t\t\\revert Score.SpacingSpanner #'strict-note-spacing\n\t\t\\revert Score.SpacingSpanner #'uniform-stretching\n\t}\n}"
    #assert t.format == "\\new Staff {\n\t{\n\t\t\\override Score.SpacingSpanner #'strict-grace-spacing = ##t\n\t\t\\override Score.SpacingSpanner #'strict-note-spacing = ##t\n\t\t\\override Score.SpacingSpanner #'uniform-stretching = ##t\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t\t\\revert Score.SpacingSpanner #'strict-grace-spacing\n\t\t\\revert Score.SpacingSpanner #'strict-note-spacing\n\t\t\\revert Score.SpacingSpanner #'uniform-stretching\n\t}\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___37():
    '''Override LilyPond SpacingSpanner grob.
    '''

    t = Score([])
    t.override.spacing_spanner.strict_grace_spacing = True
    t.override.spacing_spanner.strict_note_spacing = True
    t.override.spacing_spanner.uniform_stretching = True

    r'''
    \new Score \with {
        \override SpacingSpanner #'strict-grace-spacing = ##t
        \override SpacingSpanner #'strict-note-spacing = ##t
        \override SpacingSpanner #'uniform-stretching = ##t
    } <<
    >>
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Score \\with {\n\t\\override SpacingSpanner #'strict-grace-spacing = ##t\n\t\\override SpacingSpanner #'strict-note-spacing = ##t\n\t\\override SpacingSpanner #'uniform-stretching = ##t\n} <<\n>>"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___38():
    '''Override LilyPond SpanBar grob.
    '''

    score, treble, bass = scoretools.make_empty_piano_score()
    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    treble.extend(notes)
    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    bass.extend(notes)
    score.override.span_bar.color = 'red'

    r'''
    \new Score \with {
        \override SpanBar #'color = #red
    } <<
        \new PianoStaff <<
            \context Staff = "treble" {
                \clef "treble"
                c'8
                d'8
                e'8
                f'8
            }
            \context Staff = "bass" {
                \clef "bass"
                c'8
                d'8
                e'8
                f'8
            }
        >>
    >>
    '''

    assert componenttools.is_well_formed_component(score)
    assert score.format == '\\new Score \\with {\n\t\\override SpanBar #\'color = #red\n} <<\n\t\\new PianoStaff <<\n\t\t\\context Staff = "treble" {\n\t\t\t\\clef "treble"\n\t\t\tc\'8\n\t\t\td\'8\n\t\t\te\'8\n\t\t\tf\'8\n\t\t}\n\t\t\\context Staff = "bass" {\n\t\t\t\\clef "bass"\n\t\t\tc\'8\n\t\t\td\'8\n\t\t\te\'8\n\t\t\tf\'8\n\t\t}\n\t>>\n>>'


def test_LilyPondGrobOverrideComponentPlugIn___setattr___39():
    '''Override LilyPond StaffSymbol grob.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.override.staff_symbol.color = 'red'

    r'''
    \new Staff \with {
        \override StaffSymbol #'color = #red
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert t.format == "\\new Staff \\with {\n\t\\override StaffSymbol #'color = #red\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___40():
    '''Override LilyPond StaffSymbol grob.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t[2].override.staff.staff_symbol.color = 'red'

    r'''
    \new Staff {
        c'8
        d'8
        \once \override Staff.StaffSymbol #'color = #red
        e'8
        f'8
    }
    '''

    t.format == "\\new Staff {\n\tc'8\n\td'8\n\t\\once \\override Staff.StaffSymbol #'color = #red\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___41():
    '''Override LilyPond StaffSymbol grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.override.staff_symbol.line_positions = schemetools.SchemeVector(-4, -2, 2, 4)

    r'''
    \new Staff \with {
        \override StaffSymbol #'line-positions = #'(-4 -2 2 4)
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert staff.format == "\\new Staff \\with {\n\t\\override StaffSymbol #'line-positions = #'(-4 -2 2 4)\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___42():
    '''Override LilyPond Stem grob.
    '''

    t = Note(0, (1, 16))
    t.override.stem.stroke_style = schemetools.SchemeString('grace')

    r'''
    \once \override Stem #'stroke-style = #"grace"
    c'16
    '''

    assert t.format == '\\once \\override Stem #\'stroke-style = #"grace"\nc\'16'


def test_LilyPondGrobOverrideComponentPlugIn___setattr___43():
    '''Override LilyPond StemTremolo grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.override.stem_tremolo.slope = 0.5
    staff.override.stem_tremolo.staff_padding = 2

    r'''
    \new Staff \with {
        \override StemTremolo #'slope = #0.5
        \override StemTremolo #'staff-padding = #2
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert staff.format == "\\new Staff \\with {\n\t\\override StemTremolo #'slope = #0.5\n\t\\override StemTremolo #'staff-padding = #2\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___44():
    '''Override LilyPond SystemStartBar grob.
    '''

    score = Score([scoretools.StaffGroup([Staff(notetools.make_repeated_notes(8))])])
    score.override.system_start_bar.collapse_height = 0
    score.override.system_start_bar.color = 'red'

    r'''
    \new Score \with {
        \override SystemStartBar #'collapse-height = #0
        \override SystemStartBar #'color = #red
    } <<
        \new StaffGroup <<
            \new Staff {
                c'8
                c'8
                c'8
                c'8
                c'8
                c'8
                c'8
                c'8
            }
        >>
    >>
    '''

    assert score.format == "\\new Score \\with {\n\t\\override SystemStartBar #'collapse-height = #0\n\t\\override SystemStartBar #'color = #red\n} <<\n\t\\new StaffGroup <<\n\t\t\\new Staff {\n\t\t\tc'8\n\t\t\tc'8\n\t\t\tc'8\n\t\t\tc'8\n\t\t\tc'8\n\t\t\tc'8\n\t\t\tc'8\n\t\t\tc'8\n\t\t}\n\t>>\n>>"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___45():
    '''Override LilyPond TextScript grob.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    text_script_spanner = spannertools.TextScriptSpanner(t[:])
    text_script_spanner.override.text_script.color = 'red'

    r'''
    \new Staff {
        \override TextScript #'color = #red
        c'8
        d'8
        e'8
        f'8
        \revert TextScript #'color
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t\\override TextScript #'color = #red\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\revert TextScript #'color\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___46():
    '''Override LilyPond TextSpanner grob.
    '''

    t = Staff(notetools.make_repeated_notes(4))
    p = spannertools.TextSpanner(t[:])
    p.override.text_spanner.font_shape = 'italic'

    r'''
    \new Staff {
        \override TextSpanner #'font-shape = #'italic
        c'8 \startTextSpan
        c'8
        c'8
        c'8 \stopTextSpan
        \revert TextSpanner #'font-shape
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t\\override TextSpanner #'font-shape = #'italic\n\tc'8 \\startTextSpan\n\tc'8\n\tc'8\n\tc'8 \\stopTextSpan\n\t\\revert TextSpanner #'font-shape\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___47():
    '''Override LilyPond Tie grob.
    '''

    t = Note("c'4")
    t.override.tie.color = 'red'
    assert t.format == "\\once \\override Tie #'color = #red\nc'4"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___48():
    '''Override LilyPond TimeSignature grob.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.override.time_signature.transparent = True

    r'''
    \new Staff \with {
        \override TimeSignature #'transparent = ##t
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert t.format == "\\new Staff \\with {\n\t\\override TimeSignature #'transparent = ##t\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___49():
    '''Override LilyPond TimeSignature grob.
    '''

    t = Measure((4, 8), "c'8 d'8 e'8 f'8")
    t.override.time_signature.transparent = True

    r'''
    {
        \override TimeSignature #'transparent = ##t
        \time 4/8
        c'8
        d'8
        e'8
        f'8
        \revert TimeSignature #'transparent
    }
    '''

    assert t.format == "{\n\t\\override TimeSignature #'transparent = ##t\n\t\\time 4/8\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\revert TimeSignature #'transparent\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___50():
    '''Override LilyPond TimeSignature grob.
    '''

    t = Measure((4, 8), "c'8 d'8 e'8 f'8")
    t.override.staff.time_signature.transparent = True

    r'''
    {
        \override Staff.TimeSignature #'transparent = ##t
        \time 4/8
        c'8
        d'8
        e'8
        f'8
        \revert Staff.TimeSignature #'transparent
    }
    '''

    assert t.format == "{\n\t\\override Staff.TimeSignature #'transparent = ##t\n\t\\time 4/8\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\revert Staff.TimeSignature #'transparent\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___51():
    '''Override LilyPond TrillPitchAccidental grob.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.override.trill_pitch_accidental.staff_padding = 2
    t.override.trill_pitch_accidental.Y_extent = (-1.5, 1.5)

    r'''
    \new Staff \with {
        \override TrillPitchAccidental #'Y-extent = #'(-1.5 . 1.5)
        \override TrillPitchAccidental #'staff-padding = #2
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert t.format == "\\new Staff \\with {\n\t\\override TrillPitchAccidental #'Y-extent = #'(-1.5 . 1.5)\n\t\\override TrillPitchAccidental #'staff-padding = #2\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___52():
    '''Override LilyPond TrillSpanner grob.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    p = spannertools.TrillSpanner(t[:])
    p.override.trill_spanner.color = 'red'

    r'''
    \new Voice {
        \override TrillSpanner #'color = #red
        c'8 \startTrillSpan
        d'8
        e'8
        f'8 \stopTrillSpan
        \revert TrillSpanner #'color
    }
    '''

    assert t.format == "\\new Voice {\n\t\\override TrillSpanner #'color = #red\n\tc'8 \\startTrillSpan\n\td'8\n\te'8\n\tf'8 \\stopTrillSpan\n\t\\revert TrillSpanner #'color\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___53():
    '''Override LilyPond TupletBracket grob.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    t.override.tuplet_bracket.direction = 'down'

    r'''
    \new Voice \with {
        \override TupletBracket #'direction = #down
    } {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice \\with {\n\t\\override TupletBracket #'direction = #down\n} {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___54():
    '''Override LilyPond TupletBracket grob.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    t[1].override.tuplet_bracket.direction = 'down'

    r'''
    \new Voice {
        c'8 [
        \once \override TupletBracket #'direction = #down
        d'8
        e'8
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\t\\once \\override TupletBracket #'direction = #down\n\td'8\n\te'8\n\tf'8 ]\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___55():
    '''Override LilyPond TupletNumber grob.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    t.override.tuplet_number.fraction = True

    r'''
    \override TupletNumber #'fraction = ##t
    \times 2/3 {
        c'8
        d'8
        e'8
    }
    \revert TupletNumber #'fraction
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\override TupletNumber #'fraction = ##t\n\\times 2/3 {\n\tc'8\n\td'8\n\te'8\n}\n\\revert TupletNumber #'fraction"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___56():
    '''Override LilyPond TupletNumber grob.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    t.override.tuplet_number.fraction = True

    r'''
    \new Voice \with {
        \override TupletNumber #'fraction = ##t
    } {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice \\with {\n\t\\override TupletNumber #'fraction = ##t\n} {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___57():
    '''Override LilyPond TupletNumber grob.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    t[1].override.tuplet_number.fraction = True

    r'''
    \new Voice {
        c'8 [
        \once \override TupletNumber #'fraction = ##t
        d'8
        e'8
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 [\n\t\\once \\override TupletNumber #'fraction = ##t\n\td'8\n\te'8\n\tf'8 ]\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___58():
    '''Override LilyPond TupletNumber grob.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    t.override.tuplet_number.text = markuptools.Markup('"6:4"')

    r'''
    \new Voice \with {
        \override TupletNumber #'text = \markup { "6:4" }
    } {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == '\\new Voice \\with {\n\t\\override TupletNumber #\'text = \\markup { "6:4" }\n} {\n\tc\'8 [\n\td\'8\n\te\'8\n\tf\'8 ]\n}'


def test_LilyPondGrobOverrideComponentPlugIn___setattr___59():
    '''Override LilyPond VerticalAlignment grob.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.override.vertical_alignment.staff_padding = 2
    t.override.vertical_alignment.Y_extent = (-1.5, 1.5)

    r'''
    \new Staff \with {
        \override VerticalAlignment #'Y-extent = #'(-1.5 . 1.5)
        \override VerticalAlignment #'staff-padding = #2
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert t.format == "\\new Staff \\with {\n\t\\override VerticalAlignment #'Y-extent = #'(-1.5 . 1.5)\n\t\\override VerticalAlignment #'staff-padding = #2\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___60():
    '''Override LilyPond VerticalAxis grob.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    t.override.vertical_axis_group.staff_padding = 2
    t.override.vertical_axis_group.Y_extent = (-1.5, 1.5)

    r'''
    \new Staff \with {
        \override VerticalAxisGroup #'Y-extent = #'(-1.5 . 1.5)
        \override VerticalAxisGroup #'staff-padding = #2
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert t.format == "\\new Staff \\with {\n\t\\override VerticalAxisGroup #'Y-extent = #'(-1.5 . 1.5)\n\t\\override VerticalAxisGroup #'staff-padding = #2\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___61():
    '''Setting attribute on erroneous grob name raises exception.
    '''

    note = Note("c'8")
    assert py.test.raises(Exception, 'note.override.foo = True')
