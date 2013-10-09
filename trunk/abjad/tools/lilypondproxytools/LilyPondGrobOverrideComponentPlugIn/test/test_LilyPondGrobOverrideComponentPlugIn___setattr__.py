# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_LilyPondGrobOverrideComponentPlugIn___setattr___01():
    r'''Override LilyPond Accidental grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.override.accidental.color = 'red'

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

    assert testtools.compare(
        staff,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___02():
    r'''Override LilyPond Accidental grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff[1].override.accidental.color = 'red'

    r'''
    \new Staff {
        c'8
        \once \override Accidental #'color = #red
        d'8
        e'8
        f'8
    }
    '''

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            \once \override Accidental #'color = #red
            d'8
            e'8
            f'8
        }
        '''
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___03():
    r'''Override LilyPond BarNumber grob.
    '''

    score = Score([Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    score.override.bar_number.break_visibility = schemetools.Scheme('end-of-line-invisible')

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

    assert inspect(score).is_well_formed()
    assert testtools.compare(
        score,
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
        )

def test_LilyPondGrobOverrideComponentPlugIn___setattr___04():
    r'''Override LilyPond BarNumber grob.
    '''

    score = Score([Staff("c'8 d'8 e'8 f'8")])
    score.override.bar_number.color = 'red'

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

    assert inspect(score).is_well_formed()
    assert testtools.compare(
        score,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___05():
    r'''Override LilyPond Beam grob.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(voice[:])
    beam.override.beam.positions = (4, 4)

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

    assert testtools.compare(
        voice,
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
        )

def test_LilyPondGrobOverrideComponentPlugIn___setattr___06():
    r'''Override LilyPond Clef grob.
    '''

    note = Note("c'4")
    note.override.clef.color = 'red'

    r'''
    \once \override Clef #'color = #red
    c'4
    '''

    assert testtools.compare(
        note,
        r'''
        \once \override Clef #'color = #red
        c'4
        '''
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___07():
    r'''Override LilyPond Clef grob.
    '''

    note = Note("c'4")
    note.override.staff.clef.color = 'red'

    assert testtools.compare(
        note,
        r'''
        \once \override Staff.Clef #'color = #red
        c'4
        '''
        )
    r'''
    \once \override Staff.Clef #'color = #red
    c'4
    '''


def test_LilyPondGrobOverrideComponentPlugIn___setattr___08():
    r'''Override LilyPond Clef grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.override.clef.color = 'red'

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

    assert testtools.compare(
        staff,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___09():
    r'''Override LilyPond ClusterSpanner grob.
    '''

    cluster = containertools.Cluster(Note(1, (1, 4)) * 4)
    cluster.override.cluster_spanner.style = 'ramp'
    cluster.override.cluster_spanner.padding = 0.1

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

    assert testtools.compare(
        cluster,
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
        )

    del(cluster.override.cluster_spanner)

    r'''
    \makeClusters {
        cs'4
        cs'4
        cs'4
        cs'4
    }
    '''

    assert testtools.compare(
        cluster,
        r'''
        \makeClusters {
            cs'4
            cs'4
            cs'4
            cs'4
        }
        '''
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___10():
    r'''Override LilyPond DynamicLineSpanner grob.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    hairpin = spannertools.HairpinSpanner(voice[:], 'p < f')
    hairpin.override.dynamic_line_spanner.staff_padding = 4

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

    assert testtools.compare(
        voice,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___11():
    r'''Override LilyPond DynamicLineSpanner grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.override.dynamic_line_spanner.staff_padding = 2
    staff.override.dynamic_line_spanner.Y_extent = (-1.5, 1.5)

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

    assert testtools.compare(
        staff,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___12():
    r'''Override LilyPond DynamicText grob.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])
    dynamic_text_spanner = spannertools.DynamicTextSpanner(voice[:], 'f')
    dynamic_text_spanner.override.dynamic_text.thickness = 3

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

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___13():
    r'''Override LilyPond DynamicText grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.override.dynamic_text.staff_padding = 2
    staff.override.dynamic_text.Y_extent = (-1.5, 1.5)

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

    assert testtools.compare(
        staff,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___14():
    r'''Override LilyPond DynamicTextSpanner grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.override.dynamic_text_spanner.staff_padding = 2
    staff.override.dynamic_text_spanner.Y_extent = (-1.5, 1.5)

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

    assert testtools.compare(
        staff,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___15():
    r'''Override LilyPond Glissando grob.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    glissando = spannertools.GlissandoSpanner(voice[:])
    glissando.override.glissando.thickness = 3

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

    assert testtools.compare(
        voice,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___16():
    r'''Override LilyPond Hairpin grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.override.hairpin.staff_padding = 2
    staff.override.hairpin.Y_extent = (-1.5, 1.5)

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

    assert testtools.compare(
        staff,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___17():
    r'''Override LilyPond InstrumentName grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.set.instrument_name = markuptools.Markup(r'\circle { V }')
    staff.override.instrument_name.color = 'red'

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

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___18():
    r'''Override LilyPond MetronomeMark grob.
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

    assert inspect(score).is_well_formed()
    assert testtools.compare(
        score,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___19():
    r'''Override LilyPond MultiMeasureRestGrob.
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

    assert testtools.compare(
        staff,
        r'''
        \new Staff \with {
            \override MultiMeasureRest #'expand-limit = #12
        } {
            c'4
        }
        '''
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___20():
    r'''Override LilyPond NonMusicalPaperColumn grob.
    '''

    score = Score([Staff("c'8 d'8 e'8 f'8")])
    score.override.non_musical_paper_column.line_break_permission = False
    score.override.non_musical_paper_column.page_break_permission = False

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

    assert inspect(score).is_well_formed()
    assert testtools.compare(
        score,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___21():
    r'''Override LilyPond NoteColumn grob.
    '''

    note = Note("c'4")
    note.override.note_column.ignore_collision = True

    r'''
    \once \override NoteColumn #'ignore-collision = ##t
    c'4
    '''

    assert inspect(note).is_well_formed()
    assert testtools.compare(
        note,
        r'''
        \once \override NoteColumn #'ignore-collision = ##t
        c'4
        '''
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___22():
    r'''Override LilyPond NoteColumn grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.override.note_column.ignore_collision = True

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

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___23():
    r'''Override LilyPond NoteHead grob.
    '''

    note = Note(1, (1, 4))
    note.override.note_head.style = 'cross'

    assert note.override.note_head.style == 'cross'
    assert testtools.compare(
        note,
        r'''
        \once \override NoteHead #'style = #'cross
        cs'4
        '''
        )

    del(note.override.note_head.style)
    assert note.note_head.lilypond_format == "cs'"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___24():
    r'''Notehead styles are handled just like all other grob overrides.
    '''

    note = Note(1, (1, 4))
    note.override.note_head.style = 'mystrangehead'

    assert note.override.note_head.style == 'mystrangehead'
    assert testtools.compare(
        note,
        r'''
        \once \override NoteHead #'style = #'mystrangehead
        cs'4
        '''
        )

    del(note.override.note_head.style)
    assert note.note_head.lilypond_format == "cs'"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___25():
    r'''Notehead style overrides are handled just like all other
    note_head grob overrides, even for note_heads in chords.'''

    chord = Chord([1, 2, 3], (1, 4))
    chord.note_heads[0].tweak.style = 'harmonic'

    r'''
    <
        \tweak #'style #'harmonic
        cs'
        d'
        ef'
    >4
    '''

    assert testtools.compare(
        chord,
        r'''
        <
            \tweak #'style #'harmonic
            cs'
            d'
            ef'
        >4
        '''
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___26():
    r'''Notehead shape style overrides are just normal grob overrides.
    '''

    note = Note(1, (1, 4))
    note.override.note_head.style = 'triangle'

    assert note.override.note_head.style == 'triangle'
    assert testtools.compare(
        note,
        r'''
        \once \override NoteHead #'style = #'triangle
        cs'4
        '''
        )

    del(note.override.note_head.style)
    assert note.lilypond_format == "cs'4"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___27():
    r'''Notehead solfege style overrides are just normal grob overrides.
    Modern versions of LilyPond now handles solfege overrides correctly.'''

    note = Note(1, (1, 4))
    note.override.note_head.style = 'do'

    assert note.override.note_head.style == 'do'
    assert testtools.compare(
        note,
        r'''
        \once \override NoteHead #'style = #'do
        cs'4
        '''
        )

    del(note.override.note_head.style)
    assert note.lilypond_format == "cs'4"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___28():
    r'''Override LilyPond NoteHead grob.
    '''

    note = Note(13, (1, 4))
    note.override.note_head.transparent = True

    assert note.override.note_head.transparent
    assert testtools.compare(
        note,
        r'''
        \once \override NoteHead #'transparent = ##t
        cs''4
        '''
        )

    del(note.override.note_head.transparent)
    assert note.lilypond_format == "cs''4"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___29():
    r'''Override LilyPond NoteHead grob.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    voice.override.note_head.color = 'red'

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

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___30():
    r'''Override LilyPond OctavationBracket grob.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    octavation_spanner = spannertools.OctavationSpanner(voice[:], 1)
    octavation_spanner.override.staff.ottava_bracket.staff_position = 4

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

    assert testtools.compare(
        voice,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___31():
    r'''Override LilyPond RehearsalMark grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.override.rehearsal_mark.staff_padding = 2
    staff.override.rehearsal_mark.Y_extent = (-1.5, 1.5)

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

    assert testtools.compare(
        staff,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___32():
    r'''Override LilyPond Rest grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.override.rest.transparent = True

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

    assert testtools.compare(
        staff,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___33():
    r'''Override LilyPond Script grob.
    '''

    note = Note("c'4")
    marktools.Articulation('staccato')(note)
    note.override.script.color = 'red'

    r'''
    \once \override Script #'color = #red
    c'4 -\staccato
    '''

    assert testtools.compare(
        note,
        r'''
        \once \override Script #'color = #red
        c'4 -\staccato
        '''
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___34():
    r'''Override LilyPond Script grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.override.script.staff_padding = 2
    staff.override.script.Y_extent = (-1.5, 1.5)

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

    assert testtools.compare(
        staff,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___35():
    r'''Override LilyPond SpacingSpanner grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(staff[:])
    beam.override.score.spacing_spanner.strict_grace_spacing = True
    beam.override.score.spacing_spanner.strict_note_spacing = True
    beam.override.score.spacing_spanner.uniform_stretching = True

    r'''
    \new Staff {
        \override Score.SpacingSpanner #'strict-grace-spacing = ##t
        \override Score.SpacingSpanner #'strict-note-spacing = ##t
        \override Score.SpacingSpanner #'uniform-stretching = ##t
        c'8 [
        d'8
        e'8
        f'8 ]
        \revert Score.SpacingSpanner #'strict-grace-spacing
        \revert Score.SpacingSpanner #'strict-note-spacing
        \revert Score.SpacingSpanner #'uniform-stretching
    }
    '''

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \override Score.SpacingSpanner #'strict-grace-spacing = ##t
            \override Score.SpacingSpanner #'strict-note-spacing = ##t
            \override Score.SpacingSpanner #'uniform-stretching = ##t
            c'8 [
            d'8
            e'8
            f'8 ]
            \revert Score.SpacingSpanner #'strict-grace-spacing
            \revert Score.SpacingSpanner #'strict-note-spacing
            \revert Score.SpacingSpanner #'uniform-stretching
        }
        '''
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___36():
    r'''Override LilyPond SpacingSpanner grob on Abjad containers.
    LilyPond SpacingSpanner lives at Score by default.
    Abjad SpacingSpanner overrides usually
    require context promotion.
    '''

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beam = spannertools.BeamSpanner(staff[:])
    beam.override.score.spacing_spanner.strict_grace_spacing = True
    beam.override.score.spacing_spanner.strict_note_spacing = True
    beam.override.score.spacing_spanner.uniform_stretching = True
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                \override Score.SpacingSpanner #'strict-grace-spacing = ##t
                \override Score.SpacingSpanner #'strict-note-spacing = ##t
                \override Score.SpacingSpanner #'uniform-stretching = ##t
                c'8 [
                d'8
            }
            {
                \time 2/8
                e'8
                f'8 ]
                \revert Score.SpacingSpanner #'strict-grace-spacing
                \revert Score.SpacingSpanner #'strict-note-spacing
                \revert Score.SpacingSpanner #'uniform-stretching
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_LilyPondGrobOverrideComponentPlugIn___setattr___37():
    r'''Override LilyPond SpacingSpanner grob.
    '''

    score = Score([])
    score.override.spacing_spanner.strict_grace_spacing = True
    score.override.spacing_spanner.strict_note_spacing = True
    score.override.spacing_spanner.uniform_stretching = True

    assert testtools.compare(
        score,
        r'''
        \new Score \with {
            \override SpacingSpanner #'strict-grace-spacing = ##t
            \override SpacingSpanner #'strict-note-spacing = ##t
            \override SpacingSpanner #'uniform-stretching = ##t
        } <<
        >>
        '''
        )

    assert inspect(score).is_well_formed()


def test_LilyPondGrobOverrideComponentPlugIn___setattr___38():
    r'''Override LilyPond SpanBar grob.
    '''

    score, treble, bass = scoretools.make_empty_piano_score()
    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    treble.extend(notes)
    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    bass.extend(notes)
    score.override.span_bar.color = 'red'

    assert testtools.compare(
        score,
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
        )

    assert inspect(score).is_well_formed()


def test_LilyPondGrobOverrideComponentPlugIn___setattr___39():
    r'''Override LilyPond StaffSymbol grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.override.staff_symbol.color = 'red'

    assert testtools.compare(
        staff,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___40():
    r'''Override LilyPond StaffSymbol grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff[2].override.staff.staff_symbol.color = 'red'

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            d'8
            \once \override Staff.StaffSymbol #'color = #red
            e'8
            f'8
        }
        '''
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___41():
    r'''Override LilyPond StaffSymbol grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.override.staff_symbol.line_positions = \
        schemetools.SchemeVector(-4, -2, 2, 4)

    assert testtools.compare(
        staff,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___42():
    r'''Override LilyPond Stem grob.
    '''

    note = Note(0, (1, 16))
    note.override.stem.stroke_style = \
        schemetools.Scheme('grace', force_quotes=True)

    assert testtools.compare(
        note,
        r'''
        \once \override Stem #'stroke-style = #"grace"
        c'16
        '''
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___43():
    r'''Override LilyPond StemTremolo grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.override.stem_tremolo.slope = 0.5
    staff.override.stem_tremolo.staff_padding = 2

    assert testtools.compare(
        staff,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___44():
    r'''Override LilyPond SystemStartBar grob.
    '''

    score = Score([scoretools.StaffGroup([Staff(notetools.make_repeated_notes(8))])])
    score.override.system_start_bar.collapse_height = 0
    score.override.system_start_bar.color = 'red'

    assert testtools.compare(
        score,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___45():
    r'''Override LilyPond TextScript grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    text_script_spanner = spannertools.TextScriptSpanner(staff[:])
    text_script_spanner.override.text_script.color = 'red'

    assert testtools.compare(
        staff,
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
        )

    assert inspect(staff).is_well_formed()


def test_LilyPondGrobOverrideComponentPlugIn___setattr___46():
    r'''Override LilyPond TextSpanner grob.
    '''

    staff = Staff(notetools.make_repeated_notes(4))
    text_spanner = spannertools.TextSpanner(staff[:])
    text_spanner.override.text_spanner.font_shape = 'italic'

    assert testtools.compare(
        staff,
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
        )

    assert inspect(staff).is_well_formed()


def test_LilyPondGrobOverrideComponentPlugIn___setattr___47():
    r'''Override LilyPond Tie grob.
    '''

    note = Note("c'4")
    note.override.tie.color = 'red'

    assert testtools.compare(
        note,
        r'''
        \once \override Tie #'color = #red
        c'4
        '''
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___48():
    r'''Override LilyPond TimeSignature grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.override.time_signature.transparent = True

    assert testtools.compare(
        staff,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___49():
    r'''Override LilyPond TimeSignature grob.
    '''

    measure = Measure((4, 8), "c'8 d'8 e'8 f'8")
    measure.override.time_signature.transparent = True

    assert testtools.compare(
        measure,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___50():
    r'''Override LilyPond TimeSignature grob.
    '''

    measure = Measure((4, 8), "c'8 d'8 e'8 f'8")
    measure.override.staff.time_signature.transparent = True

    assert testtools.compare(
        measure,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___51():
    r'''Override LilyPond TrillPitchAccidental grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.override.trill_pitch_accidental.staff_padding = 2
    staff.override.trill_pitch_accidental.Y_extent = (-1.5, 1.5)

    assert testtools.compare(
        staff,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___52():
    r'''Override LilyPond TrillSpanner grob.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    trill = spannertools.TrillSpanner(voice[:])
    trill.override.trill_spanner.color = 'red'

    assert testtools.compare(
        voice,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___53():
    r'''Override LilyPond TupletBracket grob.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])
    voice.override.tuplet_bracket.direction = Down

    assert testtools.compare(
        voice,
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
        )

    assert inspect(voice).is_well_formed()


def test_LilyPondGrobOverrideComponentPlugIn___setattr___54():
    r'''Override LilyPond TupletBracket grob.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])
    voice[1].override.tuplet_bracket.direction = Down

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            \once \override TupletBracket #'direction = #down
            d'8
            e'8
            f'8 ]
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_LilyPondGrobOverrideComponentPlugIn___setattr___55():
    r'''Override LilyPond TupletNumber grob.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    tuplet.override.tuplet_number.fraction = True

    assert testtools.compare(
        tuplet,
        r'''
        \override TupletNumber #'fraction = ##t
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        \revert TupletNumber #'fraction
        '''
        )

    assert inspect(tuplet).is_well_formed()


def test_LilyPondGrobOverrideComponentPlugIn___setattr___56():
    r'''Override LilyPond TupletNumber grob.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])
    voice.override.tuplet_number.fraction = True

    assert testtools.compare(
        voice,
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
        )

    assert inspect(voice).is_well_formed()


def test_LilyPondGrobOverrideComponentPlugIn___setattr___57():
    r'''Override LilyPond TupletNumber grob.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])
    voice[1].override.tuplet_number.fraction = True

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8 [
            \once \override TupletNumber #'fraction = ##t
            d'8
            e'8
            f'8 ]
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_LilyPondGrobOverrideComponentPlugIn___setattr___58():
    r'''Override LilyPond TupletNumber grob.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])
    voice.override.tuplet_number.text = markuptools.Markup('6:4')

    assert testtools.compare(
        voice,
        r'''
        \new Voice \with {
            \override TupletNumber #'text = \markup { 6:4 }
        } {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_LilyPondGrobOverrideComponentPlugIn___setattr___59():
    r'''Override LilyPond VerticalAlignment grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.override.vertical_alignment.staff_padding = 2
    staff.override.vertical_alignment.Y_extent = (-1.5, 1.5)

    assert testtools.compare(
        staff,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___60():
    r'''Override LilyPond VerticalAxis grob.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.override.vertical_axis_group.staff_padding = 2
    staff.override.vertical_axis_group.Y_extent = (-1.5, 1.5)

    assert testtools.compare(
        staff,
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
        )


def test_LilyPondGrobOverrideComponentPlugIn___setattr___61():
    r'''InputSetExpression attribute on erroneous grob name raises exception.
    '''

    note = Note("c'8")
    assert py.test.raises(Exception, 'note.override.foo = True')
