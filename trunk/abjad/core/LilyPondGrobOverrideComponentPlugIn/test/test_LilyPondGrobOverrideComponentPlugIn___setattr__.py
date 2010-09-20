from abjad import *


def test_LilyPondGrobOverrideComponentPlugIn___setattr___01( ):
   '''Override LilyPond Accidental grob.
   '''

   t = Staff(macros.scale(4))
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___02( ):
   '''Override LilyPond Accidental grob.
   '''

   t = Staff(macros.scale(4))
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___03( ):
   '''Override LilyPond BarNumber grob.
   '''

   t = Score([Staff(macros.scale(4))])
   #t.bar_number.color = 'red'
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___04( ):
   '''Override LilyPond Clef grob.
   '''

   t = Note(0, (1, 4))
   t.override.clef.color = 'red'

   r'''
   \once \override Clef #'color = #red
   c'4
   '''

   assert t.format == "\\once \\override Clef #'color = #red\nc'4"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___05( ):
   '''Override LilyPond Clef grob.
   '''

   t = Note(0, (1, 4))
   t.override.staff.clef.color = 'red'

   assert t.format == "\\once \\override Staff.Clef #'color = #red\nc'4"
   r'''
   \once \override Staff.Clef #'color = #red
   c'4
   '''


def test_LilyPondGrobOverrideComponentPlugIn___setattr___06( ):
   '''Override LilyPond Clef grob.
   '''

   t = Staff(macros.scale(4))
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___07( ):
   '''Override LilyPond ClusterSpanner grob.
   '''

   t = chordtools.Cluster(Note(1, (1, 4)) * 4)
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___08( ):
   '''Override LilyPond DynamicLineSpanner grob.
   '''

   t = Staff(macros.scale(4))
   #t.dynamic_line_spanner.staff_padding = 2
   #t.dynamic_line_spanner.Y_extent = (-1.5, 1.5)
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___09( ):
   '''Override LilyPond DynamicText grob.
   '''

   t = Staff(macros.scale(4))
   #t.dynamic_text.staff_padding = 2
   #t.dynamic_text.Y_extent = (-1.5, 1.5)
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___10( ):
   '''Override LilyPond DynamicTextSpanner grob.
   '''

   t = Staff(macros.scale(4))
   #t.dynamic_text_spanner.staff_padding = 2
   #t.dynamic_text_spanner.Y_extent = (-1.5, 1.5)
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___11( ):
   '''Override LilyPond Hairpin grob.
   '''

   t = Staff(macros.scale(4))
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___12( ):
   '''Override LilyPond InstrumentName grob.
   '''

   t = Staff(macros.scale(4))
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___13( ):
   '''Override LilyPond MultiMeasureRestGrob.
   '''

   staff = Staff([Note(0, (1, 4))])
   staff.override.multi_measure_rest.expand_limit = 12

   r'''
   \new Staff \with {
      \override MultiMeasureRest #'expand-limit = #12
   } {
      c'4
   }
   '''

   assert staff.format == "\\new Staff \\with {\n\t\\override MultiMeasureRest #'expand-limit = #12\n} {\n\tc'4\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___14( ):
   '''Override LilyPond NonMusicalPaperColumn grob.
   '''

   t = Score([Staff(macros.scale(4))])
   #t.non_musical_paper_column.line_break_permission = False
   #t.non_musical_paper_column.page_break_permission = False
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___15( ):
   '''Override LilyPond NoteColumn grob.
   '''

   t = Note(0, (1, 4))
   #t.note_column.ignore_collision = True
   t.override.note_column.ignore_collision = True

   r'''
   \once \override NoteColumn #'ignore-collision = ##t
   c'4
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\once \\override NoteColumn #'ignore-collision = ##t\nc'4"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___16( ):
   '''Override LilyPond NoteColumn grob.
   '''

   t = Staff(macros.scale(4))
   #t.note_column.ignore_collision = True
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___17( ):
   '''Override LilyPond NoteHead grob.
   '''

   t = Voice(macros.scale(4))
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___18( ):
   '''Override LilyPond RehearsalMark grob.
   '''

   t = Staff(macros.scale(4))
   #t.rehearsal_mark.staff_padding = 2
   #t.rehearsal_mark.Y_extent = (-1.5, 1.5)
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___19( ):
   '''Override LilyPond Rest grob.
   '''

   t = Staff(macros.scale(4))
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___20( ):
   '''Override LilyPond Script grob.
   '''

   t = Note(0, (1, 4))
   t.articulations.append('staccato')
   #t.articulations.color = 'red'
   t.override.script.color = 'red'

   r'''
   \once \override Script #'color = #red
   c'4 -\staccato
   '''

   assert t.format == "\\once \\override Script #'color = #red\nc'4 -\\staccato"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___21( ):
   '''Override LilyPond Script grob.
   '''

   t = Staff(macros.scale(4))
   #t.script.staff_padding = 2
   #t.script.Y_extent = (-1.5, 1.5)
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___22( ):
   '''Override LilyPond SpacingSpanner grob.
   '''

   t = Score([ ])
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___23( ):
   '''Override LilyPond SpanBar grob.
   '''

   score, treble, bass = scoretools.make_empty_piano_score( )
   treble.extend(macros.scale(4))
   bass.extend(macros.scale(4))
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___24( ):
   '''Override LilyPond StaffSymbol grob.
   '''

   t = Staff(macros.scale(4))
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___25( ):
   '''Override LilyPond StaffSymbol grob.
   '''

   t = Staff(macros.scale(4))
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___26( ):
   '''Override LilyPond StaffSymbol grob.
   '''

   staff = Staff(macros.scale(4))
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___27( ):
   '''Override LilyPond StemTremolo grob.
   '''

   t = Staff(macros.scale(4))
   #t.stem_tremolo.staff_padding = 2
   #t.stem_tremolo.Y_extent = (-1.5, 1.5)
   t.override.stem_tremolo.staff_padding = 2
   t.override.stem_tremolo.Y_extent = (-1.5, 1.5)

   r'''
   \new Staff \with {
           \override StemTremolo #'Y-extent = #'(-1.5 . 1.5)
           \override StemTremolo #'staff-padding = #2
   } {
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert t.format == "\\new Staff \\with {\n\t\\override StemTremolo #'Y-extent = #'(-1.5 . 1.5)\n\t\\override StemTremolo #'staff-padding = #2\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_LilyPondGrobOverrideComponentPlugIn___setattr___28( ):
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___29( ):
   '''Override LilyPond TimeSignature grob.
   '''

   t = Staff(macros.scale(4))
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___30( ):
   '''Override LilyPond TimeSignature grob.
   '''

   t = Measure((4, 8), macros.scale(4))
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___31( ):
   '''Override LilyPond TimeSignature grob.
   '''

   t = Measure((4, 8), macros.scale(4))
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___32( ):
   '''Override LilyPond TrillPitchAccidental grob.
   '''

   t = Staff(macros.scale(4))
   #t.trill_pitch_accidental.staff_padding = 2
   #t.trill_pitch_accidental.Y_extent = (-1.5, 1.5)
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___33( ):
   '''Override LilyPond TupletBracket grob.
   '''

   t = Voice(macros.scale(4))
   spannertools.BeamSpanner(t[:])
   #t.tuplet_bracket.direction = 'down'
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___34( ):
   '''Override LilyPond TupletBracket grob.
   '''

   t = Voice(macros.scale(4))
   spannertools.BeamSpanner(t[:])
   #t[1].tuplet_bracket.direction = 'down'
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___35( ):
   '''Override LilyPond TupletNumber grob.
   '''

   t = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
   #t.tuplet_number.fraction = True
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___36( ):
   '''Override LilyPond TupletNumber grob.
   '''

   t = Voice(macros.scale(4))
   spannertools.BeamSpanner(t[:])
   #t.tuplet_number.fraction = True
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___37( ):
   '''Override LilyPond TupletNumber grob.
   '''

   t = Voice(macros.scale(4))
   spannertools.BeamSpanner(t[:])
   #t[1].tuplet_number.fraction = True
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___38( ):
   '''Override LilyPond TupletNumber grob.
   '''

   t = Voice(macros.scale(4))
   spannertools.BeamSpanner(t[:])
   #t.tuplet_number.text = markuptools.Markup('"6:4"')
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___39( ):
   '''Override LilyPond VerticalAlignment grob.
   '''

   t = Staff(macros.scale(4))
   #t.vertical_alignment.staff_padding = 2
   #t.vertical_alignment.Y_extent = (-1.5, 1.5)
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


def test_LilyPondGrobOverrideComponentPlugIn___setattr___40( ):
   '''Override LilyPond VerticalAxis grob.
   '''

   t = Staff(macros.scale(4))
   #t.vertical_axis_group.staff_padding = 2
   #t.vertical_axis_group.Y_extent = (-1.5, 1.5)
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
