lilypond_version = "2.19.24"

engravers = {
    "Accidental_engraver": {
        "grobs_created": set([
            "Accidental",
            "AccidentalCautionary",
            "AccidentalPlacement",
            "AccidentalSuggestion",
            ]),
        "properties_read": set([
            "accidentalGrouping",
            "autoAccidentals",
            "autoCautionaries",
            "extraNatural",
            "harmonicAccidentals",
            "internalBarNumber",
            "keyAlterations",
            "localAlterations",
            ]),
        "properties_written": set([
            "localAlterations",
            ]),
    },
    "Ambitus_engraver": {
        "grobs_created": set([
            "AccidentalPlacement",
            "Ambitus",
            "AmbitusAccidental",
            "AmbitusLine",
            "AmbitusNoteHead",
            ]),
        "properties_read": set([
            "keyAlterations",
            "middleCClefPosition",
            "middleCOffset",
            ]),
        "properties_written": set([]),
    },
    "Arpeggio_engraver": {
        "grobs_created": set([
            "Arpeggio",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Auto_beam_engraver": {
        "grobs_created": set([
            "Beam",
            ]),
        "properties_read": set([
            "autoBeaming",
            "baseMoment",
            "beamExceptions",
            "beamHalfMeasure",
            "beatStructure",
            "subdivideBeams",
            ]),
        "properties_written": set([]),
    },
    "Axis_group_engraver": {
        "grobs_created": set([
            "VerticalAxisGroup",
            ]),
        "properties_read": set([
            "currentCommandColumn",
            "hasAxisGroup",
            "keepAliveInterfaces",
            ]),
        "properties_written": set([
            "hasAxisGroup",
            ]),
    },
    "Balloon_engraver": {
        "grobs_created": set([
            "BalloonTextItem",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Bar_engraver": {
        "grobs_created": set([
            "BarLine",
            ]),
        "properties_read": set([
            "whichBar",
            ]),
        "properties_written": set([
            "forbidBreak",
            ]),
    },
    "Bar_number_engraver": {
        "grobs_created": set([
            "BarNumber",
            ]),
        "properties_read": set([
            "alternativeNumberingStyle",
            "barNumberFormatter",
            "barNumberVisibility",
            "currentBarNumber",
            "stavesFound",
            "whichBar",
            ]),
        "properties_written": set([
            "currentBarNumber",
            ]),
    },
    "Beam_collision_engraver": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Beam_engraver": {
        "grobs_created": set([
            "Beam",
            ]),
        "properties_read": set([
            "baseMoment",
            "beamMelismaBusy",
            "beatStructure",
            "subdivideBeams",
            ]),
        "properties_written": set([
            "forbidBreak",
            ]),
    },
    "Beam_performer": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Bend_engraver": {
        "grobs_created": set([
            "BendAfter",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Break_align_engraver": {
        "grobs_created": set([
            "BreakAlignGroup",
            "BreakAlignment",
            "LeftEdge",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Breathing_sign_engraver": {
        "grobs_created": set([
            "BreathingSign",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Chord_name_engraver": {
        "grobs_created": set([
            "ChordName",
            ]),
        "properties_read": set([
            "chordChanges",
            "chordNameExceptions",
            "chordNameExceptions",
            "chordNameFunction",
            "chordNoteNamer",
            "chordRootNamer",
            "lastChord",
            "majorSevenSymbol",
            "noChordSymbol",
            ]),
        "properties_written": set([
            "lastChord",
            ]),
    },
    "Chord_tremolo_engraver": {
        "grobs_created": set([
            "Beam",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Clef_engraver": {
        "grobs_created": set([
            "Clef",
            "ClefModifier",
            ]),
        "properties_read": set([
            "clefGlyph",
            "clefPosition",
            "clefTransposition",
            "clefTranspositionStyle",
            "explicitClefVisibility",
            "forceClef",
            ]),
        "properties_written": set([]),
    },
    "Cluster_spanner_engraver": {
        "grobs_created": set([
            "ClusterSpanner",
            "ClusterSpannerBeacon",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Collision_engraver": {
        "grobs_created": set([
            "NoteCollision",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Completion_heads_engraver": {
        "grobs_created": set([
            "NoteHead",
            "Tie",
            "TieColumn",
            ]),
        "properties_read": set([
            "completionFactor",
            "completionUnit",
            "measureLength",
            "measurePosition",
            "middleCPosition",
            "timing",
            ]),
        "properties_written": set([
            "completionBusy",
            ]),
    },
    "Completion_rest_engraver": {
        "grobs_created": set([
            "Rest",
            ]),
        "properties_read": set([
            "completionFactor",
            "completionUnit",
            "measureLength",
            "measurePosition",
            "middleCPosition",
            ]),
        "properties_written": set([
            "restCompletionBusy",
            ]),
    },
    "Concurrent_hairpin_engraver": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Control_track_performer": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Cue_clef_engraver": {
        "grobs_created": set([
            "ClefModifier",
            "CueClef",
            "CueEndClef",
            ]),
        "properties_read": set([
            "clefTransposition",
            "cueClefGlyph",
            "cueClefPosition",
            "cueClefTransposition",
            "cueClefTranspositionStyle",
            "explicitCueClefVisibility",
            "middleCCuePosition",
            ]),
        "properties_written": set([]),
    },
    "Custos_engraver": {
        "grobs_created": set([
            "Custos",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Default_bar_line_engraver": {
        "grobs_created": set([]),
        "properties_read": set([
            "automaticBars",
            "barAlways",
            "defaultBarType",
            "measureLength",
            "measurePosition",
            "timing",
            "whichBar",
            ]),
        "properties_written": set([]),
    },
    "Dot_column_engraver": {
        "grobs_created": set([
            "DotColumn",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Dots_engraver": {
        "grobs_created": set([
            "Dots",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Double_percent_repeat_engraver": {
        "grobs_created": set([
            "DoublePercentRepeat",
            "DoublePercentRepeatCounter",
            ]),
        "properties_read": set([
            "countPercentRepeats",
            "measureLength",
            "repeatCountVisibility",
            ]),
        "properties_written": set([
            "forbidBreak",
            ]),
    },
    "Drum_note_performer": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Drum_notes_engraver": {
        "grobs_created": set([
            "NoteHead",
            "Script",
            ]),
        "properties_read": set([
            "drumStyleTable",
            ]),
        "properties_written": set([]),
    },
    "Dynamic_align_engraver": {
        "grobs_created": set([
            "DynamicLineSpanner",
            ]),
        "properties_read": set([
            "currentMusicalColumn",
            ]),
        "properties_written": set([]),
    },
    "Dynamic_engraver": {
        "grobs_created": set([
            "DynamicText",
            "DynamicTextSpanner",
            "Hairpin",
            ]),
        "properties_read": set([
            "crescendoSpanner",
            "crescendoText",
            "currentMusicalColumn",
            "decrescendoSpanner",
            "decrescendoText",
            ]),
        "properties_written": set([]),
    },
    "Dynamic_performer": {
        "grobs_created": set([]),
        "properties_read": set([
            "dynamicAbsoluteVolumeFunction",
            "instrumentEqualizer",
            "midiInstrument",
            "midiMaximumVolume",
            "midiMinimumVolume",
            ]),
        "properties_written": set([]),
    },
    "Engraver": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Episema_engraver": {
        "grobs_created": set([
            "Episema",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Extender_engraver": {
        "grobs_created": set([
            "LyricExtender",
            ]),
        "properties_read": set([
            "extendersOverRests",
            ]),
        "properties_written": set([]),
    },
    "Figured_bass_engraver": {
        "grobs_created": set([
            "BassFigure",
            "BassFigureAlignment",
            "BassFigureBracket",
            "BassFigureContinuation",
            "BassFigureLine",
            ]),
        "properties_read": set([
            "figuredBassAlterationDirection",
            "figuredBassCenterContinuations",
            "figuredBassFormatter",
            "ignoreFiguredBassRest",
            "implicitBassFigures",
            "useBassFigureExtenders",
            ]),
        "properties_written": set([]),
    },
    "Figured_bass_position_engraver": {
        "grobs_created": set([
            "BassFigureAlignmentPositioning",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Fingering_column_engraver": {
        "grobs_created": set([
            "FingeringColumn",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Fingering_engraver": {
        "grobs_created": set([
            "Fingering",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Font_size_engraver": {
        "grobs_created": set([]),
        "properties_read": set([
            "fontSize",
            ]),
        "properties_written": set([]),
    },
    "Footnote_engraver": {
        "grobs_created": set([
            "FootnoteItem",
            "FootnoteSpanner",
            ]),
        "properties_read": set([
            "currentMusicalColumn",
            ]),
        "properties_written": set([]),
    },
    "Forbid_line_break_engraver": {
        "grobs_created": set([]),
        "properties_read": set([
            "busyGrobs",
            ]),
        "properties_written": set([
            "forbidBreak",
            ]),
    },
    "Fretboard_engraver": {
        "grobs_created": set([
            "FretBoard",
            ]),
        "properties_read": set([
            "chordChanges",
            "defaultStrings",
            "highStringOne",
            "maximumFretStretch",
            "minimumFret",
            "noteToFretFunction",
            "predefinedDiagramTable",
            "stringTunings",
            "tablatureFormat",
            ]),
        "properties_written": set([]),
    },
    "Glissando_engraver": {
        "grobs_created": set([
            "Glissando",
            ]),
        "properties_read": set([
            "glissandoMap",
            ]),
        "properties_written": set([]),
    },
    "Grace_auto_beam_engraver": {
        "grobs_created": set([
            "Beam",
            ]),
        "properties_read": set([
            "autoBeaming",
            ]),
        "properties_written": set([]),
    },
    "Grace_beam_engraver": {
        "grobs_created": set([
            "Beam",
            ]),
        "properties_read": set([
            "baseMoment",
            "beamMelismaBusy",
            "beatStructure",
            "subdivideBeams",
            ]),
        "properties_written": set([]),
    },
    "Grace_engraver": {
        "grobs_created": set([]),
        "properties_read": set([
            "graceSettings",
            ]),
        "properties_written": set([]),
    },
    "Grace_spacing_engraver": {
        "grobs_created": set([
            "GraceSpacing",
            ]),
        "properties_read": set([
            "currentMusicalColumn",
            ]),
        "properties_written": set([]),
    },
    "Grid_line_span_engraver": {
        "grobs_created": set([
            "GridLine",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Grid_point_engraver": {
        "grobs_created": set([
            "GridPoint",
            ]),
        "properties_read": set([
            "gridInterval",
            ]),
        "properties_written": set([]),
    },
    "Grob_pq_engraver": {
        "grobs_created": set([]),
        "properties_read": set([
            "busyGrobs",
            ]),
        "properties_written": set([
            "busyGrobs",
            ]),
    },
    "Horizontal_bracket_engraver": {
        "grobs_created": set([
            "HorizontalBracket",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Hyphen_engraver": {
        "grobs_created": set([
            "LyricHyphen",
            "LyricSpace",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Instrument_name_engraver": {
        "grobs_created": set([
            "InstrumentName",
            ]),
        "properties_read": set([
            "currentCommandColumn",
            "instrumentName",
            "shortInstrumentName",
            "shortVocalName",
            "vocalName",
            ]),
        "properties_written": set([]),
    },
    "Instrument_switch_engraver": {
        "grobs_created": set([
            "InstrumentSwitch",
            ]),
        "properties_read": set([
            "instrumentCueName",
            ]),
        "properties_written": set([]),
    },
    "Keep_alive_together_engraver": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Key_engraver": {
        "grobs_created": set([
            "KeyCancellation",
            "KeySignature",
            ]),
        "properties_read": set([
            "createKeyOnClefChange",
            "explicitKeySignatureVisibility",
            "extraNatural",
            "keyAlterationOrder",
            "keyAlterations",
            "lastKeyAlterations",
            "middleCClefPosition",
            "printKeyCancellation",
            ]),
        "properties_written": set([
            "keyAlterations",
            "lastKeyAlterations",
            "tonic",
            ]),
    },
    "Key_performer": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Kievan_ligature_engraver": {
        "grobs_created": set([
            "KievanLigature",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Laissez_vibrer_engraver": {
        "grobs_created": set([
            "LaissezVibrerTie",
            "LaissezVibrerTieColumn",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Ledger_line_engraver": {
        "grobs_created": set([
            "LedgerLineSpanner",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Ligature_bracket_engraver": {
        "grobs_created": set([
            "LigatureBracket",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Lyric_engraver": {
        "grobs_created": set([
            "LyricText",
            ]),
        "properties_read": set([
            "ignoreMelismata",
            "lyricMelismaAlignment",
            "searchForVoice",
            ]),
        "properties_written": set([]),
    },
    "Lyric_performer": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Mark_engraver": {
        "grobs_created": set([
            "RehearsalMark",
            ]),
        "properties_read": set([
            "markFormatter",
            "rehearsalMark",
            "stavesFound",
            ]),
        "properties_written": set([]),
    },
    "Measure_grouping_engraver": {
        "grobs_created": set([
            "MeasureGrouping",
            ]),
        "properties_read": set([
            "baseMoment",
            "beatStructure",
            "currentMusicalColumn",
            "measurePosition",
            ]),
        "properties_written": set([]),
    },
    "Melody_engraver": {
        "grobs_created": set([
            "MelodyItem",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Mensural_ligature_engraver": {
        "grobs_created": set([
            "MensuralLigature",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Metronome_mark_engraver": {
        "grobs_created": set([
            "MetronomeMark",
            ]),
        "properties_read": set([
            "currentCommandColumn",
            "currentMusicalColumn",
            "metronomeMarkFormatter",
            "stavesFound",
            "tempoHideNote",
            ]),
        "properties_written": set([]),
    },
    "Midi_control_function_performer": {
        "grobs_created": set([]),
        "properties_read": set([
            "midiBalance",
            "midiChorusLevel",
            "midiExpression",
            "midiPanPosition",
            "midiReverbLevel",
            ]),
        "properties_written": set([]),
    },
    "Multi_measure_rest_engraver": {
        "grobs_created": set([
            "MultiMeasureRest",
            "MultiMeasureRestNumber",
            "MultiMeasureRestText",
            ]),
        "properties_read": set([
            "currentCommandColumn",
            "internalBarNumber",
            "measurePosition",
            "restNumberThreshold",
            ]),
        "properties_written": set([]),
    },
    "New_fingering_engraver": {
        "grobs_created": set([
            "Fingering",
            "Script",
            "StringNumber",
            "StrokeFinger",
            ]),
        "properties_read": set([
            "fingeringOrientations",
            "harmonicDots",
            "stringNumberOrientations",
            "strokeFingerOrientations",
            ]),
        "properties_written": set([]),
    },
    "Note_head_line_engraver": {
        "grobs_created": set([
            "VoiceFollower",
            ]),
        "properties_read": set([
            "followVoice",
            ]),
        "properties_written": set([]),
    },
    "Note_heads_engraver": {
        "grobs_created": set([
            "NoteHead",
            ]),
        "properties_read": set([
            "middleCPosition",
            "staffLineLayoutFunction",
            ]),
        "properties_written": set([]),
    },
    "Note_name_engraver": {
        "grobs_created": set([
            "NoteName",
            ]),
        "properties_read": set([
            "printOctaveNames",
            ]),
        "properties_written": set([]),
    },
    "Note_performer": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Note_spacing_engraver": {
        "grobs_created": set([
            "NoteSpacing",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Ottava_spanner_engraver": {
        "grobs_created": set([
            "OttavaBracket",
            ]),
        "properties_read": set([
            "currentMusicalColumn",
            "middleCOffset",
            "ottavation",
            ]),
        "properties_written": set([]),
    },
    "Output_property_engraver": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Page_turn_engraver": {
        "grobs_created": set([]),
        "properties_read": set([
            "minimumPageTurnLength",
            "minimumRepeatLengthForPageTurn",
            ]),
        "properties_written": set([]),
    },
    "Paper_column_engraver": {
        "grobs_created": set([
            "NonMusicalPaperColumn",
            "PaperColumn",
            ]),
        "properties_read": set([
            "forbidBreak",
            ]),
        "properties_written": set([
            "currentCommandColumn",
            "currentMusicalColumn",
            "forbidBreak",
            ]),
    },
    "Parenthesis_engraver": {
        "grobs_created": set([
            "ParenthesesItem",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Part_combine_engraver": {
        "grobs_created": set([
            "CombineTextScript",
            ]),
        "properties_read": set([
            "aDueText",
            "partCombineTextsOnNote",
            "printPartCombineTexts",
            "soloIIText",
            "soloText",
            ]),
        "properties_written": set([]),
    },
    "Percent_repeat_engraver": {
        "grobs_created": set([
            "PercentRepeat",
            "PercentRepeatCounter",
            ]),
        "properties_read": set([
            "countPercentRepeats",
            "currentCommandColumn",
            "repeatCountVisibility",
            ]),
        "properties_written": set([]),
    },
    "Phrasing_slur_engraver": {
        "grobs_created": set([
            "PhrasingSlur",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Piano_pedal_align_engraver": {
        "grobs_created": set([
            "SostenutoPedalLineSpanner",
            "SustainPedalLineSpanner",
            "UnaCordaPedalLineSpanner",
            ]),
        "properties_read": set([
            "currentCommandColumn",
            ]),
        "properties_written": set([]),
    },
    "Piano_pedal_engraver": {
        "grobs_created": set([
            "PianoPedalBracket",
            "SostenutoPedal",
            "SustainPedal",
            "UnaCordaPedal",
            ]),
        "properties_read": set([
            "currentCommandColumn",
            "pedalSostenutoStrings",
            "pedalSostenutoStyle",
            "pedalSustainStrings",
            "pedalSustainStyle",
            "pedalUnaCordaStrings",
            "pedalUnaCordaStyle",
            ]),
        "properties_written": set([]),
    },
    "Piano_pedal_performer": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Pitch_squash_engraver": {
        "grobs_created": set([]),
        "properties_read": set([
            "squashedPosition",
            ]),
        "properties_written": set([]),
    },
    "Pitched_trill_engraver": {
        "grobs_created": set([
            "TrillPitchAccidental",
            "TrillPitchGroup",
            "TrillPitchHead",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Pure_from_neighbor_engraver": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Repeat_acknowledge_engraver": {
        "grobs_created": set([]),
        "properties_read": set([
            "doubleRepeatSegnoType",
            "doubleRepeatType",
            "endRepeatSegnoType",
            "endRepeatType",
            "repeatCommands",
            "segnoType",
            "startRepeatSegnoType",
            "startRepeatType",
            "whichBar",
            ]),
        "properties_written": set([]),
    },
    "Repeat_tie_engraver": {
        "grobs_created": set([
            "RepeatTie",
            "RepeatTieColumn",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Rest_collision_engraver": {
        "grobs_created": set([
            "RestCollision",
            ]),
        "properties_read": set([
            "busyGrobs",
            ]),
        "properties_written": set([]),
    },
    "Rest_engraver": {
        "grobs_created": set([
            "Rest",
            ]),
        "properties_read": set([
            "middleCPosition",
            ]),
        "properties_written": set([]),
    },
    "Rhythmic_column_engraver": {
        "grobs_created": set([
            "NoteColumn",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Scheme_engraver": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Script_column_engraver": {
        "grobs_created": set([
            "ScriptColumn",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Script_engraver": {
        "grobs_created": set([
            "Script",
            ]),
        "properties_read": set([
            "scriptDefinitions",
            ]),
        "properties_written": set([]),
    },
    "Script_row_engraver": {
        "grobs_created": set([
            "ScriptRow",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Separating_line_group_engraver": {
        "grobs_created": set([
            "StaffSpacing",
            ]),
        "properties_read": set([
            "createSpacing",
            ]),
        "properties_written": set([
            "hasStaffSpacing",
            ]),
    },
    "Slash_repeat_engraver": {
        "grobs_created": set([
            "DoubleRepeatSlash",
            "RepeatSlash",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Slur_engraver": {
        "grobs_created": set([
            "Slur",
            ]),
        "properties_read": set([
            "doubleSlurs",
            "slurMelismaBusy",
            ]),
        "properties_written": set([]),
    },
    "Slur_performer": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Spacing_engraver": {
        "grobs_created": set([
            "SpacingSpanner",
            ]),
        "properties_read": set([
            "currentCommandColumn",
            "currentMusicalColumn",
            "proportionalNotationDuration",
            ]),
        "properties_written": set([]),
    },
    "Span_arpeggio_engraver": {
        "grobs_created": set([
            "Arpeggio",
            ]),
        "properties_read": set([
            "connectArpeggios",
            ]),
        "properties_written": set([]),
    },
    "Span_bar_engraver": {
        "grobs_created": set([
            "SpanBar",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Span_bar_stub_engraver": {
        "grobs_created": set([
            "SpanBarStub",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Spanner_break_forbid_engraver": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Staff_collecting_engraver": {
        "grobs_created": set([]),
        "properties_read": set([
            "stavesFound",
            ]),
        "properties_written": set([
            "stavesFound",
            ]),
    },
    "Staff_performer": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Staff_symbol_engraver": {
        "grobs_created": set([
            "StaffSymbol",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Stanza_number_align_engraver": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Stanza_number_engraver": {
        "grobs_created": set([
            "StanzaNumber",
            ]),
        "properties_read": set([
            "stanza",
            ]),
        "properties_written": set([]),
    },
    "Stem_engraver": {
        "grobs_created": set([
            "Flag",
            "Stem",
            "StemStub",
            "StemTremolo",
            ]),
        "properties_read": set([
            "stemLeftBeamCount",
            "stemRightBeamCount",
            "whichBar",
            ]),
        "properties_written": set([]),
    },
    "System_start_delimiter_engraver": {
        "grobs_created": set([
            "SystemStartBar",
            "SystemStartBrace",
            "SystemStartBracket",
            "SystemStartSquare",
            ]),
        "properties_read": set([
            "currentCommandColumn",
            "systemStartDelimiter",
            "systemStartDelimiterHierarchy",
            ]),
        "properties_written": set([]),
    },
    "Tab_note_heads_engraver": {
        "grobs_created": set([
            "TabNoteHead",
            ]),
        "properties_read": set([
            "defaultStrings",
            "fretLabels",
            "highStringOne",
            "middleCPosition",
            "minimumFret",
            "noteToFretFunction",
            "stringOneTopmost",
            "stringTunings",
            "tabStaffLineLayoutFunction",
            "tablatureFormat",
            ]),
        "properties_written": set([]),
    },
    "Tab_staff_symbol_engraver": {
        "grobs_created": set([
            "StaffSymbol",
            ]),
        "properties_read": set([
            "stringTunings",
            ]),
        "properties_written": set([]),
    },
    "Tab_tie_follow_engraver": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Tempo_performer": {
        "grobs_created": set([]),
        "properties_read": set([
            "tempoWholesPerMinute",
            ]),
        "properties_written": set([]),
    },
    "Text_engraver": {
        "grobs_created": set([
            "TextScript",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Text_spanner_engraver": {
        "grobs_created": set([
            "TextSpanner",
            ]),
        "properties_read": set([
            "currentMusicalColumn",
            ]),
        "properties_written": set([]),
    },
    "Tie_engraver": {
        "grobs_created": set([
            "Tie",
            "TieColumn",
            ]),
        "properties_read": set([
            "skipTypesetting",
            "tieWaitForNote",
            ]),
        "properties_written": set([
            "tieMelismaBusy",
            ]),
    },
    "Tie_performer": {
        "grobs_created": set([]),
        "properties_read": set([
            "tieWaitForNote",
            ]),
        "properties_written": set([
            "tieMelismaBusy",
            ]),
    },
    "Time_signature_engraver": {
        "grobs_created": set([
            "TimeSignature",
            ]),
        "properties_read": set([
            "initialTimeSignatureVisibility",
            "partialBusy",
            "timeSignatureFraction",
            ]),
        "properties_written": set([]),
    },
    "Time_signature_performer": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Timing_translator": {
        "grobs_created": set([]),
        "properties_read": set([
            "baseMoment",
            "currentBarNumber",
            "internalBarNumber",
            "measureLength",
            "measurePosition",
            "timeSignatureFraction",
            ]),
        "properties_written": set([
            "baseMoment",
            "currentBarNumber",
            "internalBarNumber",
            "measureLength",
            "measurePosition",
            "timeSignatureFraction",
            ]),
    },
    "Translator": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Trill_spanner_engraver": {
        "grobs_created": set([
            "TrillSpanner",
            ]),
        "properties_read": set([
            "currentCommandColumn",
            "currentMusicalColumn",
            ]),
        "properties_written": set([]),
    },
    "Tuplet_engraver": {
        "grobs_created": set([
            "TupletBracket",
            "TupletNumber",
            ]),
        "properties_read": set([
            "tupletFullLength",
            "tupletFullLengthNote",
            ]),
        "properties_written": set([]),
    },
    "Tweak_engraver": {
        "grobs_created": set([]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Vaticana_ligature_engraver": {
        "grobs_created": set([
            "DotColumn",
            "VaticanaLigature",
            ]),
        "properties_read": set([]),
        "properties_written": set([]),
    },
    "Vertical_align_engraver": {
        "grobs_created": set([
            "VerticalAlignment",
            ]),
        "properties_read": set([
            "alignAboveContext",
            "alignBelowContext",
            "hasAxisGroup",
            ]),
        "properties_written": set([]),
    },
    "Volta_engraver": {
        "grobs_created": set([
            "VoltaBracket",
            "VoltaBracketSpanner",
            ]),
        "properties_read": set([
            "repeatCommands",
            "stavesFound",
            "voltaSpannerDuration",
            ]),
        "properties_written": set([]),
    },
    }
